import pytest
from services.data_fetcher import ShelterDataFetcher

def test_fetch_real_open_data():
    fetcher = ShelterDataFetcher()
    # 我們預期抓回來的資料是一組清單
    data = fetcher.get_data()
    
    assert len(data) > 0
    # 驗證關鍵欄位，這對之後的 3D 地圖至關重要
    assert "name" in data[0]
    assert "lat" in data[0]
    assert "lon" in data[0]