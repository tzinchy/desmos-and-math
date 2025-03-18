# Используем официальный образ Python 3.12-slim
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код и скрипт запуска
COPY . .

# Делаем скрипт запуска исполняемым
RUN chmod +x start.sh

# Открываем порт для Streamlit
EXPOSE 8501

# Используем скрипт запуска как команду по умолчанию
CMD ["./start.sh"]