from services.data_fetcher import DataFetcher

def test_fetcher_load_data():
    # Arrange
    fetcher = DataFetcher()

    # Act
    shelters = fetcher.get_shelters()

    # Assert
    assert len(shelters) > 0, "警告：沒讀到任何資料，請檢查 data_for_refuge 資料夾"

    first = shelters[0]
    assert first.name is not None
    assert isinstance(first.total_vessel, int)
    assert isinstance(first.lat, float)
    assert isinstance(first.lon, float)

    print(f"\n--- 測試讀取結果 ---")
    print(f"總共讀取到 {len(shelters)} 筆避難所資料")
    print(f"第一筆：{first.name}，容量：{first.total_vessel}，座標：({first.lat}, {first.lon})")
    print(f"-------------------\n")

if __name__ == "__main__":
    test_fetcher_load_data()