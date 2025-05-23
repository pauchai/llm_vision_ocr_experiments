FROM python:3.12-slim
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

EXPOSE 7860
ENTRYPOINT  ["python", "main.py"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]