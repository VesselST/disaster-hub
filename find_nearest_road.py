import psycopg2

DB_CONFIG = {
    "host": "db",
    "database": "disaster_db",
    "user": "ian",
    "password": "Qwerty12345"
}

def find_nearest_road(user_lon, user_lat):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        #將使用者輸入的經緯度轉為 point物件
        # 計算點與geom的距離
        # 遠到近排序 取距離最小值
        query = """
            SELECT name, area, ST_Distance(geom, ST_GeomFromText(%s, 4326)) as distance
            FROM roads
            ORDER BY distance ASC
            LIMIT 3;
        """
        
        user_point = f"POINT({user_lon} {user_lat})"
        cur.execute(query, (user_point,))
        result = cur.fetchone()

        if result:
            name, area, dist = result
            dist_meters = dist * 111000 #度轉距
            
            print("\n --- 避難導引 ---")
            print(f"ur in ：({user_lon}, {user_lat})")
            print(f"the area：{area}")
            print(f"the nearest main road：【{name}】")
            print(f"about {dist_meters:.1f} m")
            print("--------------------------")
        else:
            print("no data found")

    except Exception as e:
        print(f"search error {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    print("welcom to use nearest road finder")
    try:
        u_lon = input("enter your  (ex 121.524): ")
        u_lat = input("enter your latitude (ex 25.044): ")
        find_nearest_road(u_lon, u_lat)
    except ValueError:
        print("pls enter the correct number format")