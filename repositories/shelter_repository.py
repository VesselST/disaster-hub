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

    def get_all_shelters(self):
        conn = None
        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()
            # 撈取資料
            # 修改這行
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