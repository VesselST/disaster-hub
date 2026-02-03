# services/map_service.py

class MapService:
    def prepare_3d_data(self, shelters):
        """
        將 Shelter 物件轉換為 3D 繪圖需要的字典格式
        """
        return [
            {
                "name": s.name,
                "lat": s.lat,
                "lon": s.lon,
                "z": s.total_vessel, # 這裡決定 3D 柱子的高度
                "ppl": s.total_people
            }
            for s in shelters
        ]