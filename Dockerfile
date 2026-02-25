FROM python:3.10-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 升級 pip 並安裝後端依賴
RUN pip install --upgrade pip
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    plotly \
    pandas \
    pytest \
    requests \
    psycopg2-binary

COPY . .

# 使用 8501 埠啟動 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8501", "--reload"]