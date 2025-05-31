#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Функция для вывода сообщений
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

# Определение архитектуры и ОС
detect_system() {
    log "Определение системы и архитектуры..."
    
    ARCH=$(uname -m)
    OS=$(uname -s)
    
    log "Архитектура: $ARCH"
    log "Операционная система: $OS"
    
    # Проверка поддерживаемой архитектуры
    case $ARCH in
        x86_64|amd64|arm64|aarch64|armv7l)
            log "Архитектура $ARCH поддерживается"
            ;;
        *)
            error "Архитектура $ARCH не поддерживается"
            exit 1
            ;;
    esac
}

# Проверка наличия необходимых утилит
check_requirements() {
    log "Проверка необходимых утилит..."
    
    REQUIRED_TOOLS="docker curl make"
    MISSING_TOOLS=""
    
    for tool in $REQUIRED_TOOLS; do
        if ! command -v $tool &> /dev/null; then
            MISSING_TOOLS="$MISSING_TOOLS $tool"
        fi
    done
    
    if [ ! -z "$MISSING_TOOLS" ]; then
        error "Не установлены следующие утилиты:$MISSING_TOOLS"
        error "Установите их командой: sudo apt install -y$MISSING_TOOLS"
        exit 1
    fi
    
    # Проверка версий
    DOCKER_VERSION=$(docker --version | cut -d ' ' -f3 | cut -d ',' -f1)
    COMPOSE_VERSION=$(docker compose version --short 2>/dev/null || echo "не установлен")
    
    log "Docker версия: $DOCKER_VERSION"
    log "Docker Compose версия: $COMPOSE_VERSION"

    # Проверка наличия docker compose
    if ! docker compose version &> /dev/null; then
        error "Docker Compose не установлен или установлен некорректно"
        error "Установите его командой: sudo apt install -y docker-compose-plugin"
        exit 1
    fi
}

# Проверка наличия файла .env.prod
check_env_file() {
    log "Проверка файла .env.prod..."
    
    if [ ! -f .env.prod ]; then
        error "Файл .env.prod не найден"
        error "Создайте файл .env.prod с необходимыми переменными окружения"
        exit 1
    fi
    
    # Проверка необходимых переменных
    required_vars=("DJANGO_SECRET_KEY" "POSTGRES_DB" "POSTGRES_USER" "POSTGRES_PASSWORD")
    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=" .env.prod; then
            error "В файле .env.prod отсутствует переменная ${var}"
            exit 1
        fi
    done
    
    # Проверка прав доступа
    if [ "$(stat -c %a .env.prod)" != "600" ]; then
        warning "Небезопасные права доступа на файл .env.prod"
        chmod 600 .env.prod
        log "Права доступа исправлены на 600"
    fi
}

# Создание необходимых директорий
create_directories() {
    log "Создание необходимых директорий..."
    
    DIRS=(
        "docker_compose/nginx/conf"
        "docker_compose/nginx/logs"
        "static"
        "media"
        "logs"
    )
    
    for dir in "${DIRS[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log "Создана директория: $dir"
        fi
    done
    
    # Установка правильных прав
    find . -type d -exec chmod 755 {} \;
    find . -type f -exec chmod 644 {} \;
    chmod 600 .env.prod
}

# Проверка свободного места
check_disk_space() {
    log "Проверка свободного места на диске..."
    
    # Минимальное требуемое место (в МБ)
    MIN_SPACE=5000
    
    # Получаем свободное место в МБ
    FREE_SPACE=$(df -m . | awk 'NR==2 {print $4}')
    
    if [ "$FREE_SPACE" -lt "$MIN_SPACE" ]; then
        error "Недостаточно свободного места на диске. Требуется минимум ${MIN_SPACE}MB, доступно ${FREE_SPACE}MB"
        exit 1
    fi
    
    log "Доступно ${FREE_SPACE}MB свободного места"
}

# Остановка и удаление старых контейнеров
cleanup() {
    log "Очистка старых контейнеров..."
    
    if docker compose -f docker_compose/docker-compose.prod.yaml ps -q | grep -q .; then
        make prod-down || true
    fi
    
    # Очистка неиспользуемых ресурсов
    docker system prune -f --volumes
}

# Сборка новых образов
build_images() {
    log "Сборка Docker образов..."
    
    # Проверка наличия Dockerfile
    if [ ! -f "Dockerfile" ]; then
        error "Dockerfile не найден"
        exit 1
    fi
    
    # Сборка с учетом архитектуры
    if ! DOCKER_BUILDKIT=1 make build-prod; then
        error "Ошибка при сборке образов"
        exit 1
    fi
}

# Запуск контейнеров
start_containers() {
    log "Запуск контейнеров..."
    
    if ! make app-prod; then
        error "Ошибка при запуске контейнеров"
        docker compose -f docker_compose/docker-compose.prod.yaml logs
        exit 1
    fi
}

# Проверка работоспособности
health_check() {
    log "Проверка работоспособности приложения..."
    
    # Ждем 30 секунд для запуска всех сервисов
    log "Ожидание запуска сервисов..."
    sleep 30
    
    # Проверяем health endpoint
    MAX_RETRIES=5
    RETRY_DELAY=10
    
    for i in $(seq 1 $MAX_RETRIES); do
        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health/)
        
        if [ "$response" == "200" ]; then
            log "Приложение успешно запущено!"
            return 0
        else
            warning "Попытка $i из $MAX_RETRIES. Код ответа: $response"
            if [ $i -lt $MAX_RETRIES ]; then
                log "Повторная попытка через $RETRY_DELAY секунд..."
                sleep $RETRY_DELAY
            fi
        fi
    done
    
    error "Приложение не отвечает после $MAX_RETRIES попыток"
    error "Проверьте логи контейнеров:"
    docker compose -f docker_compose/docker-compose.prod.yaml logs
    exit 1
}

# Основная функция деплоя
deploy() {
    log "Начало процесса деплоя..."
    
    detect_system
    check_requirements
    check_disk_space
    check_env_file
    create_directories
    cleanup
    build_images
    start_containers
    health_check
    
    log "Деплой успешно завершен!"
    log "Приложение доступно по адресу: http://localhost"
}

# Запуск деплоя
mkdir -p logs
chmod 755 logs
deploy 