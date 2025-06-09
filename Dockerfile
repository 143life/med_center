FROM python:3.12.10-alpine

# Создаем непривилегированного пользователя
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Не создавать питоновские кэш-файлы
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.project.settings.prod

# Рабочая (корневая) директория для тома (volume)
WORKDIR /app

# Бинарники и зависимости
RUN apk update && \
    apk add --no-cache \
    python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap \
    build-base \
    libffi-dev \
    openssl-dev \
    # Добавляем Nginx
    nginx \
    # Утилиты для мониторинга
    htop \
    curl

# Установка файла pyproject.toml для загрузки зависимостей с помощью poetry
COPY pyproject.toml poetry.lock /app/

# Установка poetry и зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi --only main

# Создаем необходимые директории и устанавливаем права
RUN mkdir -p /app/static /app/media /app/logs && \
    touch /app/logs/django.log && \
    chown -R appuser:appgroup /app && \
    chmod -R 755 /app/static /app/media && \
    chmod -R 777 /app/logs

# Копируем код приложения
COPY --chown=appuser:appgroup . /app/

# Скрипт запуска
COPY --chown=appuser:appgroup entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Переключаемся на непривилегированного пользователя
USER appuser

# Определяем порты
EXPOSE 8000

# Запускаем приложение
ENTRYPOINT ["/entrypoint.sh"]