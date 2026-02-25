import psycopg2
import random

def init():
    try:
        conn = psycopg2.connect(
            dbname="disaster_db",
            user="ian",
            password="Qwerty12345",
            host="disaster_db"
        )
        cur = conn.cursor()

        # 1. 確保 PostGIS 擴充功能已開啟
        cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

        # 2. 建立資料表 (如果不存在)
        cur.execute("DROP TABLE IF EXISTS shelters;")
        cur.execute("""
            CREATE TABLE shelters (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                capacity INTEGER,
                current_ppl INTEGER,
                geom GEOMETRY(Point, 4326)
            );
        """)

        # 3. 注入 41 筆範例資料
        for i in range(1, 42):
            name = f"避難所_{i:02d}"
            cap = random.randint(100, 500)
            curr = random.randint(0, cap)
            # 台灣經緯度範圍
            lat = round(random.uniform(24.95, 25.10), 6)
            lon = round(random.uniform(121.40, 121.55), 6)
            
            cur.execute("""
                INSERT INTO shelters (name, capacity, current_ppl, geom)
                VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));
            """, (name, cap, curr, lon, lat))

        conn.commit()
        print(" 成功重新注入 41 筆避難所資料！")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"注入失敗: {e}")

if __name__ == "__main__":
    init()