import requests

class ShelterDataFetcher:
    def __init__(self):
        # 內政部消防署避難收容所 API (範例網址，實務上會依據 OpenData 調整)
        self.api_url = "https://data.moi.gov.tw/MoiBackend/api/Data/Generic/Get?id=D15000-000049"

    def get_data(self):
        try:
            # 加上 timeout 避免 AI 模擬時卡死
            response = requests.get(self.api_url, timeout=10)
            if response.status_code == 200:
                return self._parse_data(response.json())
        except Exception as e:
            print(f"抓取失敗: {e}")
        return []

    def _parse_data(self, raw_json):
        # SOLID: 這裡只負責「轉換格式」
        clean_data = []
        # 假設 API 回傳在 'data' 欄位
        for item in raw_json.get("data", []):
            clean_data.append({
                "name": item.get("避難所名稱"),
                "lat": float(item.get("緯度")),
                "lon": float(item.get("經度")),
                "capacity": int(item.get("容納人數", 0))
            })
        return clean_data