import psycopg2
from models.shelter import Shelter 

class ShelterRepository:
    def __init__(self):
        self.params = {
            'host': 'disaster_db',
            'database': 'disaster_db',
            'user': 'ian',
            'password': 'Qwerty12345'
        }

    def get_connection(self):
        """建立並回傳資料庫連線物件"""
        return psycopg2.connect(**self.params)

    def get_all_shelters(self):
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            # 撈取資料，注意你的 table 欄位名稱需與 SQL 一致
            cur.execute("SELECT name, capacity, current_ppl, ST_X(geom), ST_Y(geom) FROM public.shelters")
            rows = cur.fetchall()
            
            all_data = []
            for row in rows:
                all_data.append(Shelter(
                    name=row[0],
                    capacity=row[1],
                    current_ppl=row[2],
                    lon=row[3],
                    lat=row[4]
                ))
            cur.close()
            return all_data
        except Exception as e:
            print(f'Database error: {e}')
            return []
        finally:
            if conn:
                conn.close()

    def upsert_shelter(self, name, lat, lon, capacity):
        """
        SOLID: 確保資料庫操作的原子性。
        注意：此處縮進必須在 Class 內。
        """
        # 注意：如果你的 table 使用 PostGIS (geom)，upsert 時也要處理 geom 轉換
        sql = """
            INSERT INTO shelters (name, lat, lon, capacity, geom)
            VALUES (%s, %s, %s, %s, ST_SetSRID(ST_Point(%s, %s), 4326))
            ON CONFLICT (name) 
            DO UPDATE SET 
                lat = EXCLUDED.lat,
                lon = EXCLUDED.lon,
                capacity = EXCLUDED.capacity,
                geom = EXCLUDED.geom;
        """
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                # 傳入參數，對應 SQL 中的 %s
                cur.execute(sql, (name, lat, lon, capacity, lon, lat))
            conn.commit()
        except Exception as e:
            print(f"資料庫更新失敗: {e}")
        finally:
            if conn:
                conn.close()