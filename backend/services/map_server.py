class MapService:
    def prepare_3d_data(self, shelters):
        #物件轉dict格式
        return [
            {
                "name": s.name,
                "lat": s.lat,
                "lon": s.lon,
                "z": s.total_vessel, 
                "ppl": s.total_people
            }
            for s in shelters
        ]