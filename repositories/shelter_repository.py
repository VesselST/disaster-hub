import os
import psycopg2
from models.shelter import Shelter

class ShelterRepository:
    def __init__(self):
        # 連接資料庫初始化參數，從環境變數讀取敏感資訊
        self.conn_params = {
            "dbname": os.environ.get("POSTGRES_DB", "disaster_db"),
            "user": os.environ.get("POSTGRES_USER", "ian"),
            "password": os.environ.get("POSTGRES_PASSWORD"),
            "host": os.environ.get("POSTGRES_HOST", "disaster_db"),
            "port": os.environ.get("POSTGRES_PORT", "5432")
        }

    def upsert_shelter(self, shelter: Shelter):
        conn = psycopg2.connect(**self.conn_params)
        try:
            with conn.cursor() as cursor:
                # postGIS INSERT 語法，將物件轉為空間資料庫格式
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
                    shelter.total_people,
                    shelter.lon,
                    shelter.lat
                ))
            conn.commit()
        finally:
            conn.close()

    def get_all_shelters(self):
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
                        total_people=row[2],
                        lat=row[3],
                        lon=row[4]
                    ))
        finally:
            conn.close()
        return shelters

    def get_shelters_in_radius(self, lat: float, lon: float, radius_km: float):
        """
        使用 PostGIS 找出中心點半徑內的避難所
        """
        conn = psycopg2.connect(**self.conn_params)
        impacted_shelters = []
        try:
            with conn.cursor() as cursor:
                # radius_km * 1000 因為 ST_DWithin 使用公尺
                sql = """
                    SELECT name, capacity, current_ppl, ST_Y(geom::geometry), ST_X(geom::geometry)
                    FROM shelters
                    WHERE ST_DWithin(
                        geom,
                        ST_SetSRID(ST_Point(%s, %s), 4326)::geography,
                        %s
                    );
                """
                cursor.execute(sql, (lon, lat, radius_km * 1000))
                rows = cursor.fetchall()
                for row in rows:
                    impacted_shelters.append({
                        "name": row[0], "capacity": row[1], "lat": row[3], "lon": row[4]
                    })
        finally:
            conn.close()
        return impacted_shelters