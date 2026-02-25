import psycopg2

try:
    conn = psycopg2.connect(
        host="db",          
        database="disaster_db",
        user="ian",         
        password="Qwerty12345" 
    )
    cur = conn.cursor()

    cur.execute("INSERT INTO scenarios (name, type) VALUES ('ian's test', 'test');")
    conn.commit()
    
    print(" success")

    cur.close()
    conn.close()
except Exception as e:
    print(f" error: {e}")