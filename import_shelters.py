import json
import psycopg2

DB_CONFIG = {
    "host": "db",
    "database": "disaster_db",
    "user": "ian",
    "password": "Qwerty12345"
}

def import_shelters():
    try:
        with open('shelters_sample.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # 清空舊資料
        cur.execute("TRUNCATE TABLE shelters;")

        for s in data:
            query = """
                INSERT INTO shelters (name, area, capacity, geom)
                VALUES (%s, %s, %s, ST_GeomFromText(%s, 4326));
            """
            cur.execute(query, (s['name'], s['area'], s['capacity'], s['geometry']))
        
        conn.commit()
        print(f"✅ 成功匯入 {len(data)} 個避難所！")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import_shelters()