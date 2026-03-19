import pytest
from services.sync_service import DataSyncService
from repositories.shelter_repository import ShelterRepository

def test_sync_data_to_db():
    repo = ShelterRepository()
    sync_service = DataSyncService()
    
    # 執行同步
    sync_service.sync()
    
    # 驗證資料庫是否不再是空的
    all_shelters = repo.get_all_shelters()
    assert len(all_shelters) == 50