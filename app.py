from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from repositories.shelter_repository import ShelterRepository
from services.map_server import MapService

app = FastAPI()

# 解決跨域問題，讓前端可以抓取資料
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = ShelterRepository()
map_service = MapService()

@app.get("/api/shelters")
async def get_shelters_data():
    # 這裡沿用你原本 app.py 裡的邏輯，但只回傳 JSON 資料
    shelters = repo.get_all_shelters()
    data = map_service.prepare_3d_data(shelters)
    return data

# 啟動指令：uvicorn backend.app:app --reload