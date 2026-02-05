from services.data_fetcher import DataFetcher
from repositories.shelter_repository import ShelterRepository

class DataSyncService:
    #初始化fetcher/repository
    def __init__(self):
        self.fetcher = DataFetcher()
        self.repository = ShelterRepository()

    def sync(self): 
        print("starting data synchronization...")
        shelters = self.fetcher.get_shelters()
        
        if not shelters:
            print("synchronization aborted, no data fetched.")
            return

        success_count = 0
        for s in shelters:
            try:
                #呼叫shelter_repository中寫的upsert_shelter函式
                self.repository.upsert_shelter(s)
                success_count += 1
            except Exception as e:
                print(f"error when upserting {s.name}: {e}")
        
        print(f"synchronization success {success_count}/{len(shelters)} times data")