import psycopg2
from models.shelter import Shelter 

class ShelterRepository:
    # 初始化資料庫連線參數
    def __init__(self):
        self.parms = {
            'host': 'disaster_db',
            'database': 'disaster_db',
            'user': 'ian',
            'password': 'Qwerty12345'
        }


    #跟資料庫連結
    def connect_database(self):
        return psycopg2.connect(**self.parms)

    #將db的二進數據轉為shelter物件
    def get_all_shelters(self):
        conn = None
        try:
            conn = self.connect_database()
            cur = conn.cursor()
            # 撈取資料
            cur.execute("SELECT name, total_people, total_vessel, ST_X(geom), ST_Y(geom) FROM public.shelters")
            rows = cur.fetchall()
            
            all_data = []
            for row in rows:
                all_data.append(Shelter(
                    name=row[0],
                    total_people=row[1],
                    total_vessel=row[2],
                    lon=row[3],
                    lat=row[4]
                ))
            cur.close()
            return all_data
            #回傳
        except Exception as e:
            print(f'Database error: {e}')
            return []
        finally:
            if conn:
                conn.close()

    #檢查重複
    def upsert_shelter(self, name, lat, lon, capacity):
        #確保一致性 將經緯度轉為空間資料
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
            print(f"database error: {e}")
        finally:
            if conn:
                conn.close()
                #避免連線樹耗盡