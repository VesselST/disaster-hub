import psycopg2

DB_CONFIG = {
    "host": "db",
    "database": "disaster_db",
    "user": "ian",
    "password": "Qwerty12345"
}

def simulate_event(center_lon, center_lat, radius_meters):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 1. 先將所有道路恢復正常 (重設模擬環境)
        cur.execute("UPDATE roads SET status = 'normal';")

        # 2. 找出半徑範圍內的道路並更新狀態為blocked
        # ST_DWithin(幾何1, 幾何2, 距離) 
        # geography(geom) 是為了讓距離單位變成公尺
        query = """
            UPDATE roads 
            SET status = 'blocked'
            WHERE ST_DWithin(
                geography(geom), 
                geography(ST_GeomFromText(%s, 4326)), 
                %s
            )
            RETURNING name, area;
        """
        
        center_point = f"POINT({center_lon} {center_lat})"
        cur.execute(query, (center_point, radius_meters))
        blocked_roads = cur.fetchall()

        conn.commit()

        print(f"\n--- 災害模擬報告 ---")
        print(f"災害中心：({center_lon}, {center_lat})")
        print(f"影響半徑：{radius_meters} 公尺")
        
        if blocked_roads:
            print(f"the road has been blocked：")
            for name, area in blocked_roads:
                print(f"    [{area}] {name}")
        else:
            print(" no road affected.")

    except Exception as e:
        print(f" error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    print(" 進入災害模擬模式")
    lon = input("輸入災害中心經度 (如 121.518): ")
    lat = input("輸入災害中心緯度 (如 25.040): ")
    radius = input("輸入影響半徑 (公尺，如 500): ")
    simulate_event(lon, lat, float(radius))