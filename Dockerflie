# 1. 升級到 Python 3.10，這對新版 Flet 的支援度更高
FROM python:3.10-slim

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libpq-dev \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. 先升級 pip，再安裝套件 (將 flet 微調至 0.21.2)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --default-timeout=100 \
    flet==0.21.2 \
    psycopg2-binary \
    requests

RUN pip install --no-cache-dir --default-timeout=100 \
    pytest \
    pandas \
    pydeck

COPY . .

CMD ["python", "app.py"]