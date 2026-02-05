import json
import os
import glob
from models.shelter import Shelter

class DataFetcher:
    def __init__(self):
        # 取得專案根目錄，指向你的 data_for_refuge 資料夾
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = os.path.normpath(os.path.join(current_dir, "..", "data_for_refuge"))

    def get_shelters(self) -> list[Shelter]:
        all_shelters = []
        
        # 自動尋找資料夾內所有 .json 檔案
        search_pattern = os.path.join(self.folder_path, "*.json")
        json_files = glob.glob(search_pattern)
        
        if not json_files:
            print(f"DEBUG: 掃描路徑為 {self.folder_path}")
            print(" 錯誤：找不到任何 JSON 檔案！")
            return []

        for file_path in json_files:
            filename = os.path.basename(file_path)
            # 取得地區名（例如 yilan_shelter.json -> YILAN）
            region_name = filename.split('_')[0].upper()
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        shelter = Shelter(
                            name=f"[{region_name}] {item.get('name')}",
                            total_vessel=int(item.get("total_vessel", 0)),
                            total_people=int(item.get("total_people", 0)),
                            lat=float(item.get("lat", 0.0)),
                            lon=float(item.get("lon", 0.0))
                        )
                        all_shelters.append(shelter)
                print(f"成功讀取 {filename}，共 {len(data)} 筆資料。")
            except Exception as e:
                print(f"解析 {filename} 失敗: {e}")

        return all_shelters