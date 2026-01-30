from services.data_fetcher import DataFetcher 
from repositories.shelter_repository import ShelterRepository

class DataSyncService:
    def __init__(self):
        #初始化組件
        self.fetcher = DataFetcher()
        self.repo = ShelterRepository()

    #讀取json並更新到資料庫
    def sync(self):
        print("starting data synchronization...")

        # 透過 fetcher 取得 shelter 物件清單 
        # new_data是shelter實例 不是dict
        new_data = self.fetcher.get_shelters()
        
        if not new_data:
            print("synchronization aborted,no data fetched.")
            return

        #遍歷清單
        success_count = 0
        for shelter in new_data:
            try:
                #用物件的方式存屬性
                self.repo.upsert_shelter(
                    name=shelter.name,
                    lat=shelter.lat,
                    lon=shelter.lon,
                    total_vessel=shelter.total_vessel
                )
                success_count += 1
            except Exception as e:
                print(f"error when upserting {shelter.name}: {e}")

        print(f"synchronization success {success_count}/{len(new_data)}times data ")