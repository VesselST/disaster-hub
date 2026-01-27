FROM python:3.9-slim

# 安裝連線資料庫與 UI 渲染所需的系統依賴
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安裝 binary 版本並讓 flet 安裝 0.21 系列中最穩定的版本
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir psycopg2-binary "flet>=0.21.0,<0.22.0"

COPY . .

EXPOSE 8501

CMD ["python", "app.py"]
