# Disaster Hub 

**AI 驅動的台灣東部災害避難所決策系統**

以 2025 年花蓮光復鄉堰塞湖災害為出發點，針對現有避難所管理系統資訊不透明、無法模擬、決策緩慢三大痛點所開發的災害模擬決策系統。


---

## 功能特色

- **真實地圖視覺化** — Leaflet.js + OpenStreetMap，宜花東 50 處避難所標記於真實座標，marker 大小依容量縮放，點擊顯示即時資訊
- **PostGIS 空間模擬** — 設定災害中心點與影響半徑，後端透過 `ST_DWithin` 計算受影響避難所清單，支援強震、淹水、火災三種類型
- **人群疏散動畫** — 模擬災害發生後人群往避難所移動的過程，負載率即時變化
- **AI 決策助手** — 整合 RAG + 本地 LLM，根據避難所真實資料回答問題，支援語意查詢、地理距離查詢、容量排序查詢

---

## 技術架構

```
資料層        PostgreSQL + PostGIS（空間資料）
              ChromaDB（語意向量索引）

後端層        FastAPI + Uvicorn
              ShelterRepository（資料庫操作）
              ChatService（RAG + LLM）
              VectorStore（ChromaDB 管理）

前端層        Leaflet.js + OpenStreetMap
              Canvas API（人群疏散動畫）
              iOS 風格 UI

容器化        Docker + Docker Compose
LLM           Ollama + llama3.2:3b（本地部署）
```

---

## 快速開始

### 環境需求

- Docker Desktop
- 16GB RAM 以上（Ollama 本地跑模型需要）

### 1. 複製專案

```bash
git clone https://github.com/VesselST/disaster-hub.git
cd disaster-hub
```

### 2. 設定環境變數

```bash
cp  .env
POSTGRES_DB=YOURDBNAME
POSTGRES_USER=YOURNAME
POSTGRES_PASSWORD=YOURPASSWORD
POSTGRES_HOST=YOURHOST
POSTGRES_PORT=YOURHOST
# 編輯 .env 填入資料庫密碼
```

### 3. 啟動服務

```bash
docker-compose up --build
```

### 4. 下載 LLM 模型（第一次需要）

```bash
docker exec -it ollama ollama pull llama3.2:3b
```



---

## 專案結構

```
Disaster_Hub/
├── app.py                      # FastAPI 主程式
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── init.sql                    # 資料庫初始化
├── .env.example
│
├── models/
│   └── shelter.py              # Shelter 資料模型
│
├── repositories/
│   └── shelter_repository.py   # 資料庫操作（含重試機制）
│
├── services/
│   ├── data_fetcher.py         # 讀取 JSON 資料
│   ├── map_server.py           # 地圖資料格式化
│   ├── sync_service.py         # 資料同步
│   ├── chat_service.py         # RAG + LLM 聊天
│   └── vector_store.py         # ChromaDB 向量索引
│
├── data_for_refuge/
│   ├── hualien_shelter.json    # 花蓮（14 筆）
│   ├── taitung_shelter.json    # 台東（16 筆）
│   └── yilan_shelter.json      # 宜蘭（20 筆）
│
├── static/
│   └── index.html              # 前端介面
│
└── tests/
    ├── test_shelter_model.py
    ├── test_map_service.py
    ├── test_data_fetcher2.py
    ├── test_api_data.py
    └── test_sync_service.py
```

---

## API 端點

| 方法 | 路徑 | 說明 |
|---|---|---|
| GET | `/api/3d_data` | 取得所有避難所資料 |
| POST | `/api/simulate_disaster` | 執行災害空間模擬 |
| POST | `/api/nearest_shelter` | 查詢最近避難所（PostGIS 距離排序）|
| POST | `/api/chat` | AI 決策助手 |
| POST | `/api/sync` | 手動觸發資料同步 |

---

## 執行測試

```bash
docker exec -it disaster_app pytest tests/ -v
```

---

## AI 查詢範例

```
花蓮哪間避難所容量最大？
→ 直接排序資料庫回傳正確結果

緯度 23.99 經度 121.60 附近哪裡最近？
→ PostGIS ST_Distance 真實地理距離排序

哪些避難所受到影響？
→ 直接讀取模擬結果，不走 RAG

目前受影響的避難所還有空間嗎？
→ RAG 語意搜尋 + 模擬 context
```

---

## 開發者

**Vessel**

