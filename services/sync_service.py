from services.data_fetcher import ShelterDataFetcher
from repositories.shelter_repository import ShelterRepository

class DataSyncService:
    def __init__(self):
        self.fetcher = ShelterDataFetcher()
        self.repo = ShelterRepository()

    def sync(self):
        # 1. 從 API 或備援機制抓取資料
        new_data = self.fetcher.get_data()
        
        # 2. 寫入資料庫 (這裡假設 repo 有實作批次插入)
        for item in new_data:
            self.repo.upsert_shelter(
                name=item['name'],
                lat=item['lat'],
                lon=item['lon'],
                capacity=item['capacity']
            )
        print(f"同步完成！共處理 {len(new_data)} 筆資料。")