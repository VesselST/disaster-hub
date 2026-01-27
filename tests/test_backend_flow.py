import pytest
from repositories.shelter_repository import ShelterRepository
from models.shelter import Shelter

def test_shelter_repository_data_integrity():
    # Arrange (準備)
    repo = ShelterRepository()
    
    # Act (執行)
    shelters = repo.get_all_shelters()
    
    # Assert (斷言/驗證)
    # 驗證是否為列表
    assert isinstance(shelters, list)
    
    # 驗證筆數是否為 41 (這是你當初匯入的數量)
    assert len(shelters) == 41, f"預期有 41 筆資料，但實際抓到 {len(shelters)} 筆"
    
    # 隨機抽取一筆驗證結構
    sample = shelters[0]
    assert isinstance(sample, Shelter)
    assert sample.name is not None
    assert isinstance(sample.lat, float)
    assert isinstance(sample.lon, float)
    assert sample.capacity > 0
    
    print(f"\n 成功驗證 {len(shelters)} 筆避難所數據完整性！")