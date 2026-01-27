import json
import psycopg2

DB_CONFIG = {
    "host": "db",
    "database": "disaster_db",
    "user": "ian",
    "password": "Qwerty12345"
}

def start_import():
    try:
        with open('roads_sample.json', 'r', encoding='utf-8') as f:
            roads_data = json.load(f)
        
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("contect success,importing data")

        cur.execute("TRUNCATE TABLE roads;")

        for road in roads_data:
            query = """
                INSERT INTO roads (name, area, geom, status)
                VALUES (%s, %s, ST_GeomFromText(%s, 4326), 'normal');
            """
            cur.execute(query, (road['Rd_Name'], road['Area'], road['geometry']))

        conn.commit()
        print(f"imported {len(roads_data)} roads successfully. ")

    except Exception as e:
        print(f"import error {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    start_import()