import os
import requests
from services.vector_store import VectorStore

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")

SYSTEM_PROMPT = """你是台灣東部災害避難所管理系統的 AI 決策助手。
你只能使用繁體中文回答，嚴格禁止使用任何英文單字、簡體中文或其他語言。
你只能根據提供的資料回答，不可以自行推測或編造資訊。
如果資料中沒有相關資訊，請說「目前沒有相關資料」。
回答要簡潔、務實，重點放在疏散建議與避難所資訊。
不要使用任何符號裝飾，不要使用 emoji。"""

class ChatService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def chat(self, user_message: str, simulation_context: str = "") -> str:
        """
        接收使用者問題，用語意搜尋撈相關資料，呼叫 Ollama 回答
        simulation_context: 可選，傳入當前模擬結果
        """
        shelter_context = self.vector_store.search(user_message)

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
                        "temperature": 0.3,  # 降低隨機性，讓回答更穩定、不亂飄
                        "num_predict": 300   # 限制回答長度，避免過長
                    }
                },
                timeout=120
            )
            result = response.json()
            return result.get("response", "無法取得回應").strip()

        except Exception as e:
            return f"AI 服務連線失敗：{e}"