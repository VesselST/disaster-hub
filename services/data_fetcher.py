# services/data_fetcher.py
import requests

class ShelterDataFetcher:
    def get_data(self):
        try:
            # 嘗試連線
            response = requests.get("https://data.moi.gov.tw/MoiBackend/api/Data/Generic/Get?id=D15000-000049", timeout=5)
            if response.status_code == 200:
                return self._parse_data(response.json())
        except:
            # 如果連不上，回傳一組「開發用備援數據」
            print("警告：API 連線失敗，啟動備援模擬數據模式")
            return [
                {"name": "台北 101 避難點 (模擬)", "lat": 25.0339, "lon": 121.5644, "capacity": 1000},
                {"name": "高雄 85 大樓 (模擬)", "lat": 22.6116, "lon": 120.3003, "capacity": 500}
            ]
        return []

    def _parse_data(self, data):
        # 這裡保留你之前的解析邏輯
        return [{"name": "真實數據", "lat": 0, "lon": 0}]