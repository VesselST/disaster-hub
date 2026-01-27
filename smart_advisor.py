import psycopg2

DB_CONFIG = {"host": "db", "database": "disaster_db", "user": "ian", "password": "Qwerty12345"}

def get_smart_advice(u_lon, u_lat):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 找出最近的 3 個避難所
    # 判斷 current_ppl < capacity (還有空位)
    # 排除周邊道路中斷的點 
    query = """
        SELECT s.name, s.area, s.capacity, s.current_ppl,
               ST_Distance(s.geom, ST_GeomFromText(%s, 4326)) * 111000 as dist_meters
        FROM shelters s
        WHERE s.current_ppl < s.capacity  -- 💡 過濾掉已經滿員的避難所
        AND NOT EXISTS (
            SELECT 1 FROM roads r 
            WHERE r.status = 'blocked' 
            AND ST_DWithin(geography(r.geom), geography(s.geom), 500)
        )
        ORDER BY dist_meters ASC
        LIMIT 1;
    """
    
    cur.execute(query, (f"POINT({u_lon} {u_lat})",))
    result = cur.fetchone()
    
    print("\n --- AI 災防指揮官決策系統 ---")
    if result:
        name, area, cap, curr, dist = result
        remaining = cap - curr
        print(f" 偵測到您的位置附近有潛在風險。")
        print(f" 最佳避難建議：前往【{name}】({area})")
        print(f" 距離您約：{dist:.1f} 公尺")
        print(f" 該處剩餘容量：{remaining} 人 (總容量 {cap} 人)")
        print("\n 指揮官提醒：該處目前尚有空間，請儘速前往。")
    else:
        print("警告：附近所有避難所皆已滿員或周邊交通中斷！")
        print(" 請立即前往高處或尋找堅固建築物就地避難，並等待進一步廣播。")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    lon = input("輸入目前經度: ")
    lat = input("輸入目前緯度: ")
    get_smart_advice(lon, lat)