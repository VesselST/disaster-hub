from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from repositories.shelter_repository import ShelterRepository
from services.map_server import MapService
from services.sync_service import DataSyncService
from services.chat_service import ChatService
from services.vector_store import VectorStore
import uvicorn

app = FastAPI()

# 1. 初始化 server / repo / services
repo = ShelterRepository()
map_service = MapService()
vector_store = VectorStore()
chat_service = ChatService(vector_store=vector_store)

# 儲存最新模擬結果（記憶體暫存）
latest_simulation: dict = {}

# 2. 啟動時同步資料 + 建立向量索引
@app.on_event("startup")
async def startup_sync():
    print("啟動時執行資料同步...")
    sync_service = DataSyncService()
    sync_service.sync()

    print("建立向量索引...")
    shelters = repo.get_all_shelters()
    vector_store.build_index(shelters)

# 3. 手動觸發同步 + 重建索引
@app.post("/api/sync")
async def manual_sync():
    sync_service = DataSyncService()
    sync_service.sync()
    shelters = repo.get_all_shelters()
    vector_store.build_index(shelters)
    return {"status": "success", "message": "資料同步與索引重建完成"}

# 4. 數據 API
@app.get("/api/3d_data")
async def get_3d_data():
    shelters = repo.get_all_shelters()
    data = map_service.prepare_3d_data(shelters)
    return data

# 5. 災害模擬 API
@app.post("/api/simulate_disaster")
async def simulate(data: dict):
    global latest_simulation

    lat = data.get('lat')
    lon = data.get('lon')
    radius = data.get('radius')
    sim_type = data.get('type', 'earthquake')

    impacted = repo.get_shelters_in_radius(lat, lon, radius)

    # 儲存模擬結果供 AI 使用
    latest_simulation = {
        "type": sim_type,
        "lat": lat,
        "lon": lon,
        "radius_km": radius,
        "impacted_count": len(impacted),
        "impacted_shelters": impacted
    }

    return {
        "status": "success",
        "impacted_count": len(impacted),
        "impacted_shelters": impacted
    }

# 6. AI 聊天 API
@app.post("/api/chat")
async def chat(data: dict):
    message = data.get("message", "")
    if not message:
        return {"status": "error", "reply": "請輸入問題"}

    # 組合模擬 context（如果有）
    sim_context = ""
    if latest_simulation:
        sim_context = (
            f"災害類型：{latest_simulation['type']}，"
            f"中心座標：({latest_simulation['lat']}, {latest_simulation['lon']})，"
            f"影響半徑：{latest_simulation['radius_km']} 公里，"
            f"受影響避難所數量：{latest_simulation['impacted_count']} 個。"
        )

    reply = chat_service.chat(message, simulation_context=sim_context)
    return {"status": "success", "reply": reply}

# 7. 渲染首頁
@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Static/index.html 檔案不存在</h1>"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501)