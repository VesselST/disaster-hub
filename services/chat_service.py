import os
import re
import requests
from services.vector_store import VectorStore

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")

SYSTEM_PROMPT = """你是台灣東部災害避難所管理系統的 AI 決策助手。
你只能使用繁體中文回答，嚴格禁止使用任何英文單字、簡體中文或其他語言。
你只能根據提供的資料回答，不可以自行推測或編造資訊。
如果資料中沒有相關資訊，請說「目前沒有相關資料」。
回答要簡潔、務實，重點放在疏散建議與避難所資訊。
不要使用任何符號裝飾，不要使用 emoji。"""

# 觸發地理搜尋的關鍵字
GEO_KEYWORDS = ["最近", "附近", "離我最近", "最靠近", "距離最近", "哪裡最近", "近的"]

class ChatService:
    def __init__(self, vector_store: VectorStore, repo=None):
        self.vector_store = vector_store
        self.repo = repo

    def _is_geo_query(self, message: str) -> bool:
        return any(kw in message for kw in GEO_KEYWORDS)

    def _extract_coords(self, message: str):
        """
        支援多種座標格式：
        - 緯度 23.99 經度 121.60
        - 23.99 121.60
        - 23.99/121.60
        - 23.99,121.60
        """
        patterns = [
            r'緯度[：:＝=\s]*([\d.]+)[,，/\s]+經度[：:＝=\s]*([\d.]+)',
            r'([\d.]+)[/,，\s]+([\d.]+)',
        ]
        for pat in patterns:
            m = re.search(pat, message)
            if m:
                try:
                    lat, lon = float(m.group(1)), float(m.group(2))
                    # 確認是台灣範圍內的座標
                    if 20 <= lat <= 26 and 119 <= lon <= 123:
                        return lat, lon
                except:
                    pass
        return None

    def _get_nearest_context(self, lat: float, lon: float) -> str:
        """
        呼叫 repo 取得最近避難所，組成文字 context 給 LLM
        """
        if self.repo is None:
            return "無法取得避難所資料（repo 未初始化）。"
        try:
            results = self.repo.get_nearest_shelters(lat, lon, limit=5)
            if not results:
                return "附近沒有找到避難所資料。"

            lines = [f"使用者位置：緯度 {lat}、經度 {lon}"]
            lines.append("距離最近的避難所（依距離由近到遠排序）：")
            for i, s in enumerate(results, 1):
                lines.append(
                    f"{i}. {s['name']}：距離 {s['distance_km']} 公里，"
                    f"容量 {s['capacity']} 人，剩餘空間 {s['remaining']} 人"
                )
            return "\n".join(lines)
        except Exception as e:
            return f"地理查詢失敗：{e}"

    def chat(self, user_message: str, simulation_context: str = "") -> str:
        """
        接收使用者問題，根據問題類型選擇 RAG 語意搜尋或 PostGIS 地理查詢
        """
        is_geo = self._is_geo_query(user_message)
        coords = self._extract_coords(user_message) if is_geo else None

        if is_geo and coords is None:
            # 有距離關鍵字但沒有座標，提示使用者提供位置
            return "請提供您的座標以便查詢最近的避難所。例如：緯度 23.99 經度 121.60"

        if is_geo and coords:
            lat, lon = coords
            shelter_context = self._get_nearest_context(lat, lon)
        else:
            # 一般語意查詢，使用 ChromaDB RAG
            shelter_context = self.vector_store.search(user_message)

        # 組合完整 prompt context
        full_context = f"【避難所資料】\n{shelter_context}"
        if simulation_context:
            full_context += f"\n\n【目前災害模擬結果】\n{simulation_context}"

        prompt = f"""{full_context}

【使用者問題】
{user_message}

注意：請用繁體中文回答，不得使用任何英文。"""

        try:
            response = requests.post(
                f"{OLLAMA_HOST}/api/generate",
                json={
                    "model": "llama3.2:3b",
                    "system": SYSTEM_PROMPT,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 300
                    }
                },
                timeout=120
            )
            result = response.json()
            return result.get("response", "無法取得回應").strip()

        except Exception as e:
            return f"AI 服務連線失敗：{e}"