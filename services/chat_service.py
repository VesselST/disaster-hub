import os
import requests
from services.vector_store import VectorStore

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")

class ChatService:
    def __init__(self, vector_store: VectorStore):
        # 接收外部傳入的 vector_store，避免重複初始化
        self.vector_store = vector_store

    def chat(self, user_message: str, simulation_context: str = "") -> str:
        """
        接收使用者問題，用語意搜尋撈相關資料，呼叫 Ollama 回答
        simulation_context: 可選，傳入當前模擬結果
        """
        # 從向量資料庫語意搜尋相關避難所
        shelter_context = self.vector_store.search(user_message)

        # 組合 context：避難所資料 + 模擬結果（如果有）
        full_context = f"【避難所資料】\n{shelter_context}"
        if simulation_context:
            full_context += f"\n\n【目前災害模擬結果】\n{simulation_context}"

        prompt = f"""你是一個台灣東部災害避難所管理系統的 AI 決策助手。
請嚴格使用繁體中文回答，絕對不可以夾雜英文或簡體中文。
不要使用 emoji。回答要簡潔、清楚，重點放在實用的疏散建議。
只根據以下提供的資料回答，如果資料中沒有相關資訊，請直接說「目前沒有相關資料」，不要自行推測。

{full_context}

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