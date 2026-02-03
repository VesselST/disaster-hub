from services.data_fetcher import DataFetcher
from repositories.shelter_repository import ShelterRepository

class DataSyncService:
    def __init__(self):
        self.fetcher = DataFetcher()
        self.repository = ShelterRepository()

    def sync(self):  # <--- 確保這個方法名稱是 sync，且縮排正確
        print("starting data synchronization...")
        shelters = self.fetcher.get_shelters()
        
        if not shelters:
            print("synchronization aborted, no data fetched.")
            return

        success_count = 0
        for s in shelters:
            try:
                # 這裡要對應你 Repository 裡面的方法名
                self.repository.upsert_shelter(s)
                success_count += 1
            except Exception as e:
                print(f"error when upserting {s.name}: {e}")
        
        print(f"synchronization success {success_count}/{len(shelters)} times data")