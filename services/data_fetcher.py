import json
import os
from models.shelter import Shelter

#指定資料路徑
class DataFetcher:
    def __init__(self):
        self.data_path = [
            "data_for_refuge\\yilan_shelters.json",
            "data_for_refuge\\hualian_shelters.json",
            "data_for_refuge\\taitung_shelters.json"
        ]

    #將本地json資料轉為sheltr物件清單
    def get_shelters(self) -> list[Shelter]:
        try:
            with open('data/data_for_refuge.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        
            all_shelters = []
            #遍歷宜花東key
            for region in ['yilan_shelter', 'hualian_shelter', 'taitung_shelter']:
                region_data = data.get(region, [])
                for item in region_data:
                        all_shelters.append(Shelter(
                        name=f"[{region[:2]}] {item['name']}", # 加上地區前綴方便識別
                        capacity=item['capacity'],
                        current_ppl=item.get('current_ppl', 0),
                        lat=item['lat'],
                        lon=item['lon']
                    ))
            return all_shelters
        except Exception as e:
            print(f"fetch data error: {e}")
        return []