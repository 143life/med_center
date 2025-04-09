FROM python:3.12.10-alpine

# Не создавать питоновские кэш-файлы
ENV PYTHONDONTWRITEBYTECODE=1
# 
ENV PYTHONNUNBUFFERED=1

# Рабочая (корневая) директория для тома (volume)
WORKDIR /app

# Бинарники
RUN apk update && \
    apk add --no-cache python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap

# Установка файла pyproject.toml для загрузки зависимостей с помощью poetry
ADD pyproject.toml /app

# Установка poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Не создавать виртуальное окружение
RUN poetry config virtualenvs.create false
# установка зависимостей
RUN poetry install --no-root --no-interaction --no-ansi

# Скопировать директорию . в WORKDIR директорию
COPY . /app/

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh