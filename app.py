from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from repositories.shelter_repository import ShelterRepository
from services.map_server import MapService
import uvicorn

app = FastAPI()

# 1. 初始化你原本的 Service 與 Repo
repo = ShelterRepository()
map_service = MapService()

# 2. 數據 API (供前端 Plotly 使用)
@app.get("/api/3d_data")
async def get_3d_data():
    shelters = repo.get_all_shelters()
    data = map_service.prepare_3d_data(shelters)
    return data

# 3. 渲染首頁 (取代 Flet 的 UI)
@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Static/index.html 檔案不存在</h1>"

# 4. 如果有靜態資源就掛載
# app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    # 強制跑在 8501
    uvicorn.run(app, host="0.0.0.0", port=8501)