import psycopg2
from models.shelter import Shelter

class ShelterRepository:
    def __init__(self):
        # 這裡請根據你的資料庫設定調整
        self.conn_params = {
            "dbname": "disaster_db",
            "user": "ian",
            "password": "Qwerty12345",
            "host": "localhost",
            "port": "5432"
        }

    def upsert_shelter(self, shelter: Shelter):
        conn = psycopg2.connect(**self.conn_params)
        try:
            with conn.cursor() as cursor:
                # 欄位對齊你的新變數名稱 total_vessel, total_poeple
                sql = """
                    INSERT INTO shelters (name, capacity, current_ppl, geom)
                    VALUES (%s, %s, %s, ST_SetSRID(ST_Point(%s, %s), 4326))
                    ON CONFLICT (name) DO UPDATE SET
                        capacity = EXCLUDED.capacity,
                        current_ppl = EXCLUDED.current_ppl,
                        geom = EXCLUDED.geom;
                """
                cursor.execute(sql, (
                    shelter.name, 
                    shelter.total_vessel, 
                    shelter.total_poeple, 
                    shelter.lon, 
                    shelter.lat
                ))
            conn.commit()
        finally:
            conn.close()

    def get_all_shelters(self):
        """供 app.py 呼叫讀取所有資料"""
        conn = psycopg2.connect(**self.conn_params)
        shelters = []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT name, capacity, current_ppl, ST_Y(geom::geometry), ST_X(geom::geometry) FROM shelters")
                rows = cursor.fetchall()
                for row in rows:
                    shelters.append(Shelter(
                        name=row[0],
                        total_vessel=row[1],
                        total_poeple=row[2],
                        lat=row[3],
                        lon=row[4]
                    ))
        finally:
            conn.close()
        return shelters