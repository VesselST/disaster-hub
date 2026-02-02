import unittest
import os
from shelter_sys import ShelterService, ShelterRepository

class TestShelterSystem(unittest.TestCase):
    def setUp(self):
        # 確保路徑指向您存放宜花東 JSON 的資料夾
        self.data_folder = "data_for_refuge"
        
        # 遵循 SOLID：如果資料夾不存在，測試應該給予提醒
        if not os.path.exists(self.data_folder):
            self.skipTest(f"找不到資料夾: {self.data_folder}")
            
        self.repo = ShelterRepository(self.data_folder)
        self.service = ShelterService(self.repo)

    def test_total_data_loaded(self):
        """測試是否成功載入了宜花東所有的資料"""
        all_data = self.repo.get_all()
        # 斷言：資料總數應該要大於 0 (表示有讀到檔案)
        self.assertGreater(len(all_data), 0, "應該要載入至少一筆避難所資料")

    def test_find_yilan_sport_center(self):
        """測試搜尋：輸入宜蘭運動公園座標，應回傳運動中心"""
        # 宜蘭運動公園座標
        user_lat, user_lon = 24.7431, 121.7565
        results = self.service.get_nearest(user_lat, user_lon, limit=1)
        
        self.assertEqual(results[0]['name'], "宜蘭市國民運動中心")
        print(f"\n找到最近避難所: {results[0]['name']}，距離: {results[0]['distance']:.2f} km")

if __name__ == '__main__':
    unittest.main()