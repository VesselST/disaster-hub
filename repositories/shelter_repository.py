import os
import time
import psycopg2
from psycopg2 import OperationalError
from models.shelter import Shelter

MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒

class ShelterRepository:
    def __init__(self):
        self.conn_params = {
            "dbname": os.environ.get("POSTGRES_DB", "disaster_db"),
            "user": os.environ.get("POSTGRES_USER", "ian"),
            "password": os.environ.get("POSTGRES_PASSWORD"),
            "host": os.environ.get("POSTGRES_HOST", "disaster_db"),
            "port": os.environ.get("POSTGRES_PORT", "5432")
        }

    def _connect(self):
        """
        建立資料庫連線，失敗時自動重試最多 3 次
        """
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return psycopg2.connect(**self.conn_params)
            except OperationalError as e:
                print(f"DB 連線失敗（第 {attempt} 次）：{e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                else:
                    raise RuntimeError(f"資料庫連線失敗，已重試 {MAX_RETRIES} 次：{e}")

    def upsert_shelter(self, shelter: Shelter):
        conn = self._connect()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO shelters (name, capacity, current_ppl, geom)
                    VALUES (%s, %s, %s, ST_SetSRID(ST_Point(%s, %s), 4326))
                    ON CONFLICT (name) DO UPDATE SET
                        capacity = EXCLUDED.capacity,
                        current_ppl = EXCLUDED.current_ppl,
                        geom = EXCLUDED.geom;
                """
                cursor.execute(sql, (
                    shelter.name,
                    shelter.total_vessel,
                    shelter.total_people,
                    shelter.lon,
                    shelter.lat
                ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"upsert_shelter 失敗：{e}")
        finally:
            conn.close()

    def get_all_shelters(self):
        conn = self._connect()
        shelters = []
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT name, capacity, current_ppl, ST_Y(geom::geometry), ST_X(geom::geometry) FROM shelters"
                )
                rows = cursor.fetchall()
                for row in rows:
                    shelters.append(Shelter(
                        name=row[0],
                        total_vessel=row[1],
                        total_people=row[2],
                        lat=row[3],
                        lon=row[4]
                    ))
        except Exception as e:
            raise RuntimeError(f"get_all_shelters 失敗：{e}")
        finally:
            conn.close()
        return shelters

    def get_shelters_in_radius(self, lat: float, lon: float, radius_km: float):
        """
        使用 PostGIS 找出中心點半徑內的避難所
        """
        conn = self._connect()
        impacted_shelters = []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT name, capacity, current_ppl, ST_Y(geom::geometry), ST_X(geom::geometry)
                    FROM shelters
                    WHERE ST_DWithin(
                        geom,
                        ST_SetSRID(ST_Point(%s, %s), 4326)::geography,
                        %s
                    );
                """
                cursor.execute(sql, (lon, lat, radius_km * 1000))
                rows = cursor.fetchall()
                for row in rows:
                    impacted_shelters.append({
                        "name": row[0], "capacity": row[1], "lat": row[3], "lon": row[4]
                    })
        except Exception as e:
            raise RuntimeError(f"get_shelters_in_radius 失敗：{e}")
        finally:
            conn.close()
        return impacted_shelters

    def get_nearest_shelters(self, lat: float, lon: float, limit: int = 5):
        """
        使用 PostGIS ST_Distance 找出距離中心點最近的 N 個避難所，依距離排序
        """
        conn = self._connect()
        nearest = []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT
                        name,
                        capacity,
                        current_ppl,
                        ST_Y(geom::geometry) AS lat,
                        ST_X(geom::geometry) AS lon,
                        ROUND(
                            ST_Distance(
                                geom::geography,
                                ST_SetSRID(ST_Point(%s, %s), 4326)::geography
                            )::numeric / 1000, 2
                        ) AS distance_km
                    FROM shelters
                    ORDER BY geom::geography <-> ST_SetSRID(ST_Point(%s, %s), 4326)::geography
                    LIMIT %s;
                """
                cursor.execute(sql, (lon, lat, lon, lat, limit))
                rows = cursor.fetchall()
                for row in rows:
                    remaining = max(0, row[1] - row[2])
                    nearest.append({
                        "name": row[0],
                        "capacity": row[1],
                        "current_ppl": row[2],
                        "remaining": remaining,
                        "lat": float(row[3]),
                        "lon": float(row[4]),
                        "distance_km": float(row[5])
                    })
        except Exception as e:
            raise RuntimeError(f"get_nearest_shelters 失敗：{e}")
        finally:
            conn.close()
        return nearest