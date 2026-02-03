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
    # repositories/shelter_repository.py

def upsert_shelter(self, shelter: Shelter):
    try:
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # 這裡的 SQL 語法要對應到你資料庫的欄位名稱
                # 假設資料庫欄位叫 capacity
                sql = """
                    INSERT INTO shelters (name, capacity, current_ppl, geom)
                    VALUES (%s, %s, %s, ST_SetSRID(ST_Point(%s, %s), 4326))
                    ON CONFLICT (name) DO UPDATE SET
                        capacity = EXCLUDED.capacity,
                        current_ppl = EXCLUDED.current_ppl,
                        geom = EXCLUDED.geom;
                """
                # 修正這裡：使用 shelter.capacity 而不是 shelter.total_vessel
                cursor.execute(sql, (
                    shelter.name, 
                    shelter.total_vessel,  # 這裡要改！
                    shelter.total_people, 
                    shelter.lon, 
                    shelter.lat
                ))
            conn.commit()
    except Exception as e:
        print(f"error when upserting {shelter.name}: {e}")