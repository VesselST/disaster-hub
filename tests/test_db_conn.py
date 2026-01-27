# test_db_conn.py
import psycopg2
import pytest

def test_database_connection():
    """
    測試 Python 容器是否能成功連線到 PostgreSQL 容器
    符合 DIP (依賴反轉)：我們先測試連線抽象，不關心具體表結構
    """
    try:
        conn = psycopg2.connect(
            host="disaster_db",  # Docker Compose 中的服務名稱
            database="disaster_db",
            user="user",
            password="password"
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        
        assert result[0] == 1
        
        cur.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"連線失敗，請檢查 Docker Compose 設定: {e}")