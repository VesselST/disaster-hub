import json
import os
from models.shelter import Shelter

class DataFetcher:
    def __init__(self):
        # 取得專案根目錄路徑
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 指向你的資料夾：data/data_for_refuge/
        self.folder_path = os.path.join(current_dir, "..", "data", "data_for_refuge")

    def get_shelters(self) -> list[Shelter]:
        all_shelters = []
        
        # 定義你要讀取的檔案清單 (確保檔名與你資料夾內的一致)
        target_files = {
            "YILAN": "yilan_shelter.json",
            "HUALIEN": "hualian_shelter.json",
            "TAITUNG": "taitung_shelter.json"
        }

        for region, filename in target_files.items():
            file_path = os.path.join(self.folder_path, filename)
            
            if not os.path.exists(file_path):
                print(f"找不到檔案: {file_path}，跳過。")
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        # 建立物件並標記地區
                        shelter = Shelter(
                            name=f"[{region}] {item.get('name')}",
                            capacity=item.get("capacity", 0),
                            current_ppl=item.get("current_ppl", 0),
                            lat=item.get("lat", 0.0),
                            lon=item.get("lon", 0.0)
                        )
                        all_shelters.append(shelter)
                print(f"✅ 成功載入 {region} 資料，共 {len(data)} 筆。")
            except Exception as e:
                print(f"讀取 {filename} 時發生錯誤: {e}")

        return all_shelters