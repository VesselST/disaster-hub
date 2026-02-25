import psycopg2

DB_CONFIG = {"host": "db", "database": "disaster_db", "user": "ian", "password": "Qwerty12345"}

def find_safe_shelter(u_lon, u_lat):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 複雜查詢：
    # 1. 找出所有避難所
    # 2. 排除掉那些「附近道路狀態為 blocked」的避難所 (假設避難所周邊路斷了就不安全)
    # 3. 按距離排序
    query = """
        SELECT s.name, s.area, ST_Distance(s.geom, ST_GeomFromText(%s, 4326)) as dist
        FROM shelters s
        WHERE NOT EXISTS (
            SELECT 1 FROM roads r 
            WHERE r.status = 'blocked' 
            AND ST_DWithin(geography(r.geom), geography(s.geom), 500)
        )
        ORDER BY dist ASC
        LIMIT 1;
    """
    
    cur.execute(query, (f"POINT({u_lon} {u_lat})",))
    result = cur.fetchone()
    
    if result:
        print(f"🚀 安全導引成功！建議前往：【{result[0]}】({result[1]})")
    else:
        print("⚠️ 警告：附近避難所周邊道路皆已中斷，請就地掩蔽或聯繫直升機救援！")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    lon = input("輸入經度: ")
    lat = input("輸入緯度: ")
    find_safe_shelter(lon, lat)