from services.data_fetcher import DataFetcher

def test_fetcher_load_data():
    # 1. 初始化 Fetcher
    fetcher = DataFetcher()
    
    # 2. 執行讀取動作
    shelters = fetcher.get_shelters()
    
    # 3. 驗證結果
    print(f"\n--- 測試讀取結果 ---")
    print(f"總共讀取到 {len(shelters)} 筆避難所資料")
    
    if len(shelters) > 0:
        first = shelters[0]
        print(f"第一筆測試範例:")
        print(f"  名稱: {first.name}")
        print(f"  容量: {first.capacity}")
        print(f"  經緯度: ({first.lat}, {first.lon})")
        print(f"-------------------\n")
    else:
        print(" 警告：沒讀到任何資料！請檢查檔案路徑或 JSON 格式。")

if __name__ == "__main__":
    test_fetcher_load_data()