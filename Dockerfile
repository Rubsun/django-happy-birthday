# Базовый образ Python
FROM python:3.10-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файлы зависимостей
COPY requirements.txt /code/

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . /code/


