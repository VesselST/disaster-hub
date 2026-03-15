import os
import requests
from repositories.shelter_repository import ShelterRepository

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")

class ChatService:
    def __init__(self):
        self.repo = ShelterRepository()

    def _get_relevant_shelters(self, query: str) -> str:
        """
        RAG 檢索：從資料庫撈出相關避難所資料
        根據 query 關鍵字過濾，組成文字 context 給 LLM
        """
        shelters = self.repo.get_all_shelters()

        # 關鍵字過濾：如果有提到地區就只回傳該地區
        keywords = {
            "宜蘭": "YILAN",
            "花蓮": "HUALIEN",
            "台東": "TAITUNG",
        }

        filtered = shelters
        for word, tag in keywords.items():
            if word in query:
                filtered = [s for s in shelters if tag in s.name]
                break

        if not filtered:
            filtered = shelters

        # 組成文字 context
        lines = []
        for s in filtered[:20]:  # 最多取 20 筆避免 context 太長
            rate = s.occupancy_rate if hasattr(s, 'occupancy_rate') else 0
            lines.append(
                f"- {s.name}：容量 {s.total_vessel} 人，"
                f"目前 {s.total_people} 人，"
                f"負載率 {rate:.1f}%"
            )

        return "\n".join(lines)

    def chat(self, user_message: str) -> str:
        """
        接收使用者問題，組合 RAG context，呼叫 Ollama 回答
        """
        context = self._get_relevant_shelters(user_message)

        prompt = prompt = f"""你是一個台灣東部災害避難所管理系統的 AI 決策助手。
請嚴格使用繁體中文回答，不可以夾雜英文或簡體中文。
不要使用 emoji。回答要簡潔、清楚，重點放在實用的疏散建議。
【目前避難所資料】
{context}

【使用者問題】
{user_message}

請用繁體中文回答："""

        try:
            response = requests.post(
                f"{OLLAMA_HOST}/api/generate",
                json={
                    "model": "llama3.2:3b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            result = response.json()
            return result.get("response", "無法取得回應").strip()

        except Exception as e:
            return f"AI 服務連線失敗：{e}"