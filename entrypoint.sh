#!/bin/sh

# функция для ожидания доступности порта
wait_for_port() {
    host=$1
    port=$2
    timeout=30  # Увеличиваем таймаут для продакшена
    start_time=$(date +%s)

    echo "Waiting for $host:$port..."
    
    # попробовать использовать nc, если установлен
    nc_command="nc"
    if ! command -v $nc_command > /dev/null 2>&1; then
        nc_command="ncat"
    fi

    while ! $nc_command -z "$host" "$port" > /dev/null 2>&1; do
        sleep 1
        current_time=$(date +%s)
        elapsed_time=$((current_time - start_time))
        echo "Trying to connect to $host:$port (elapsed: ${elapsed_time}s)"

        if [ $elapsed_time -ge $timeout ]; then
            echo "Error: Unable to connect to $host:$port after ${timeout} seconds"
            exit 1
        fi
    done
    echo "$host:$port is available"
}

# Проверка наличия необходимых переменных окружения
for var in DJANGO_SECRET_KEY POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD; do
    eval value=\$$var
    if [ -z "$value" ]; then
        echo "Error: Required environment variable $var is not set"
        exit 1
    fi
done

echo "Starting application initialization..."

# Ожидание доступности сервисов
wait_for_port "postgres" 5432
wait_for_port "redis" 6379

echo "Creating logs directory..."
# Создание директории для логов с правильными правами
mkdir -p /app/logs
chmod 777 /app/logs

echo "Checking Django configuration..."
# Проверка конфигурации Django
python manage.py check --deploy

echo "Running database migrations..."
# Применение миграций
python manage.py migrate --noinput

echo "Collecting static files..."
# Сбор статики
python manage.py collectstatic --noinput

echo "Creating cache tables..."
# Создание таблиц кэша
python manage.py createcachetable

echo "Starting Daphne server..."
# Запуск с продакшен настройками
exec daphne \
    -b 0.0.0.0 \
    -p 8000 \
    --access-log - \
    --proxy-headers \
    core.project.asgi:application