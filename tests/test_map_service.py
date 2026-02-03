import unittest
from models.shelter import Shelter
# 這是我們待會要寫的 Service
from services.map_server import MapService 

class TestMapService(unittest.TestCase):
    def test_transform_shelters_to_3d_data(self):
        # 1. Arrange (準備資料)
        mock_shelters = [
            Shelter(name="花蓮體育館", total_vessel=100, lat=23.9, lon=121.6, total_people=10),
            Shelter(name="宜蘭國小", total_vessel=200, lat=24.7, lon=121.7, total_people=50)
        ]
        service = MapService()

        # 2. Act (執行轉換)
        result = service.prepare_3d_data(mock_shelters)

        # 3. Assert (驗證結果)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], "花蓮體育館")
        self.assertEqual(result[0]['z'], 100)  # 3D 高度應該等於容量
        self.assertEqual(result[1]['lat'], 24.7)

if __name__ == '__main__':
    unittest.main()