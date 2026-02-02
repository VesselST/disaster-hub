import json
import math

# 1. 單一職責：只負責計算距離
class DistanceCalculator:
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # 地球半徑 (公里)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

# 2. 介面/資料存取層：負責讀取 JSON
class ShelterRepository:
    def __init__(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_all(self):
        return self.data

# 3. 業務邏輯層：負責搜尋與排序
class ShelterService:
    def __init__(self, repository: ShelterRepository):
        self.repository = repository
        self.calculator = DistanceCalculator()

    def get_nearest(self, lat, lon, limit=3):
        shelters = self.repository.get_all()
        
        for shelter in shelters:
            # 計算使用者與每個避難所的距離
            shelter['distance'] = self.calculator.haversine(
                lat, lon, shelter['lat'], shelter['lon']
            )
        
        # 依據距離排序
        sorted_shelters = sorted(shelters, key=lambda x: x['distance'])
        return sorted_shelters[:limit]