import chromadb
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self):
        # 使用本地持久化儲存
        self.client = chromadb.Client()
        
        # 使用預設的 sentence-transformers embedding
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        
        # 建立或取得 collection
        self.collection = self.client.get_or_create_collection(
            name="shelters",
            embedding_function=self.ef
        )

    def build_index(self, shelters: list) -> None:
        """
        將避難所資料向量化並存入 ChromaDB
        每次啟動重新建立，確保資料是最新的
        """
        if not shelters:
            print("VectorStore: 沒有資料可以建立索引")
            return

        # 清空舊資料
        existing = self.collection.get()
        if existing["ids"]:
            self.collection.delete(ids=existing["ids"])

        documents = []
        metadatas = []
        ids = []

        for i, s in enumerate(shelters):
            # 把每筆避難所轉成自然語言句子，讓 embedding 更準確
            occupancy_rate = s.occupancy_rate if hasattr(s, 'occupancy_rate') else 0.0
            remaining = s.total_vessel - s.total_people

            doc = (
                f"{s.name} 位於緯度 {s.lat}、經度 {s.lon}。"
                f"總容量為 {s.total_vessel} 人，"
                f"目前收容 {s.total_people} 人，"
                f"剩餘空間 {remaining} 人，"
                f"負載率 {occupancy_rate:.1f}%。"
            )

            documents.append(doc)
            metadatas.append({
                "name": s.name,
                "lat": s.lat,
                "lon": s.lon,
                "total_vessel": s.total_vessel,
                "total_people": s.total_people,
                "remaining": remaining,
                "occupancy_rate": round(occupancy_rate, 1)
            })
            ids.append(f"shelter_{i}")

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"VectorStore: 成功建立 {len(shelters)} 筆避難所索引")

    def search(self, query: str, n_results: int = 10) -> str:
        """
        語意搜尋：找出與 query 最相關的避難所資料
        回傳組合好的文字 context 給 LLM
        """
        total = self.collection.count()
        if total == 0:
            return "目前沒有避難所資料。"

        # 確保不超過總資料數
        n = min(n_results, total)

        results = self.collection.query(
            query_texts=[query],
            n_results=n
        )

        docs = results.get("documents", [[]])[0]
        if not docs:
            return "找不到相關避難所資料。"

        return "\n".join(f"- {doc}" for doc in docs)