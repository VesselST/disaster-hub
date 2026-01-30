import json
import os
from models.shelter import Shelter

#指定資料路徑
class DataFetcher:
    def __init__(self):
        self.data_path = "data.json"

    #將本地json資料轉為sheltr物件清單
    def get_shelters(self) -> list[Shelter]:
        if not os.path.exists(self.data_path):
            print(f"error:cannot find the dataflie {self.data_path}")
            return []

        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            shelters = []
            #將所有json所有格式轉為shelter中定義好的模型
            for item in raw_data:
                shelter = Shelter(
                    name=item.get("name"),
                    total_vessel=item.get("total_vessel", 0),
                    total_people=item.get("total_people", 0),
                    lat=item.get("lat", 0.0),
                    lon=item.get("lon", 0.0)
                )
                shelters.append(shelter)
            
            return shelters
        
        except Exception as e:
            print(f"catching json reading error: {e}")
            return []