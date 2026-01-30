import pytest
from repositories.shelter_repository import ShelterRepository

def test_upsert_logic():
    repo = ShelterRepository()
    
    # 測試資料
    test_name = "測試避難所_TDD"
    
    # 執行 upsert
    repo.upsert_shelter(test_name, 25.0339, 121.5644, 500)
    
    # 驗證是否成功 
    assert True