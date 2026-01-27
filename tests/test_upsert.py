import pytest
# 關鍵：從 repositories 資料夾下的檔案匯入類別
from repositories.shelter_repository import ShelterRepository

def test_upsert_logic():
    # 現在 Python 才知道 ShelterRepository 是什麼
    repo = ShelterRepository()
    
    # 測試資料
    test_name = "測試避難所_TDD"
    
    # 執行 Upsert
    repo.upsert_shelter(test_name, 25.0339, 121.5644, 500)
    
    # 驗證是否成功 (這裡你可以加入查詢邏輯來斷言)
    assert True