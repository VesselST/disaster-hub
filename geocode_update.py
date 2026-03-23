"""
執行方式：
1. 在本機（不是 Docker 內）安裝套件：pip install geopy
2. 把這個腳本放在 Disaster_Hub 根目錄
3. 執行：python geocode_update.py
4. 檢查輸出的三個 _fixed.json 檔案
5. 確認無誤後替換原本的 JSON 檔案
"""

import json
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

geolocator = Nominatim(user_agent="disaster_hub_geocoder", timeout=10)

FILES = [
    "data_for_refuge/hualien_shelter.json",
    "data_for_refuge/taitung_shelter.json",
    "data_for_refuge/yilan_shelter.json",
]

def geocode_address(address: str):
    """
    用地址查詢經緯度，失敗時回傳 None
    """
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"  查詢失敗：{e}")
        return None

def process_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        shelters = json.load(f)

    print(f"\n處理 {filepath}（共 {len(shelters)} 筆）")
    print("-" * 50)

    updated = 0
    failed = []

    for s in shelters:
        name = s.get("name", "")
        address = s.get("address", "")
        old_lat = s.get("lat", "")
        old_lon = s.get("lon", "")

        print(f"查詢：{name} | {address}")

        result = geocode_address(address)

        if result:
            new_lat, new_lon = result
            s["lat"] = str(round(new_lat, 6))
            s["lon"] = str(round(new_lon, 6))
            print(f"  舊：({old_lat}, {old_lon})")
            print(f"  新：({s['lat']}, {s['lon']})")
            updated += 1
        else:
            print(f"  找不到座標，保留原始值：({old_lat}, {old_lon})")
            failed.append(name)

        time.sleep(1.2)  # Nominatim 限制每秒最多 1 次請求

    # 輸出新檔案
    output_path = filepath.replace(".json", "_fixed.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(shelters, f, ensure_ascii=False, indent=4)

    print(f"\n完成：{updated}/{len(shelters)} 筆更新")
    if failed:
        print(f"以下需要手動確認：{failed}")
    print(f"輸出：{output_path}")

    return failed

if __name__ == "__main__":
    all_failed = []
    for filepath in FILES:
        failed = process_file(filepath)
        all_failed.extend(failed)

    print("\n" + "=" * 50)
    print("全部完成！")
    if all_failed:
        print(f"需要手動確認座標的地點（共 {len(all_failed)} 筆）：")
        for name in all_failed:
            print(f"  - {name}")
    else:
        print("所有地點都成功取得座標！")
    print("\n請確認 _fixed.json 的座標正確後，再替換原始 JSON 檔案。")