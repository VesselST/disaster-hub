from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from repositories.shelter_repository import ShelterRepository
from services.map_server import MapService
import os

app = FastAPI()

repo = ShelterRepository()
map_service = MapService()

# 數據接口
@app.get("/api/3d_data")
async def get_3d_data():
    shelters = repo.get_all_shelters()
    return map_service.prepare_3d_data(shelters)

# 掛載靜態檔案 
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')