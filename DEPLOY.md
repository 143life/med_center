# Инструкция по деплою Med Center

## Подготовка сервера

1. **Системные требования**:
   - Linux-based OS (Ubuntu 20.04+, Debian 10+)
   - Минимум 2 ГБ RAM
   - Минимум 10 ГБ свободного места
   - Процессор: x86_64/amd64, arm64, или arm/v7

2. **Установка Docker и Docker Compose**:
   ```bash
   # Обновление пакетов
   sudo apt update
   sudo apt upgrade -y
   
   # Установка необходимых пакетов
   sudo apt install -y \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg \
       lsb-release

   # Добавление официального GPG-ключа Docker
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

   # Добавление репозитория Docker
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

   # Установка Docker
   sudo apt update
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

   # Добавление пользователя в группу docker
   sudo usermod -aG docker $USER

   # Применение изменений группы (требуется перелогин)
   newgrp docker

   # Проверка установки
   docker --version
   docker compose version
   ```

3. **Настройка файрвола**:
   ```bash
   # Открываем необходимые порты
   sudo apt install -y ufw
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

## Подготовка проекта

1. **Клонирование репозитория**:
   ```bash
   git clone <your-repo-url>
   cd med_center
   ```

2. **Создание .env.prod файла**:
   ```bash
   # Генерация безопасного ключа
   DJANGO_SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
   
   # Создание .env.prod файла
   cat > .env.prod << EOL
   DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
   DJANGO_PORT=8000
   POSTGRES_DB=med_center
   POSTGRES_USER=med_user
   POSTGRES_PASSWORD=$(openssl rand -base64 32)
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   EOL
   
   # Установка правильных прав
   chmod 600 .env.prod
   ```

3. **Настройка домена**:
   - Добавьте A-запись в DNS:
     ```
     smtu-med.ru -> <ваш-ip>
     www.smtu-med.ru -> <ваш-ip>
     ```
   - Проверка DNS:
     ```bash
     # Проверка прямого резолвинга
     dig +short smtu-med.ru
     dig +short www.smtu-med.ru
     
     # Проверка обратного резолвинга
     dig -x <ваш-ip>
     ```

## Деплой приложения

1. **Подготовка директорий и прав**:
   ```bash
   # Создание директорий с правильными правами
   sudo mkdir -p /var/www/med_center/{static,media,logs}
   sudo chown -R $USER:$USER /var/www/med_center
   sudo chmod -R 755 /var/www/med_center
   ```

2. **Автоматический деплой**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Ручной деплой** (если автоматический не сработал):
   ```bash
   # Создание директорий
   mkdir -p docker_compose/nginx/conf
   mkdir -p docker_compose/nginx/logs
   mkdir -p static media logs

   # Сборка образов
   make build-prod

   # Запуск контейнеров
   make app-prod
   ```

## Проверка работоспособности

1. **Проверка сервисов**:
   ```bash
   # Проверка статуса контейнеров
   docker ps
   docker-compose -f docker_compose/docker-compose.prod.yaml ps

   # Проверка логов всех сервисов
   docker-compose -f docker_compose/docker-compose.prod.yaml logs

   # Проверка логов отдельных сервисов
   docker-compose -f docker_compose/docker-compose.prod.yaml logs nginx
   docker-compose -f docker_compose/docker-compose.prod.yaml logs main-app

   # Проверка health check
   curl -v http://localhost/health/
   ```

2. **Проверка доступности сайта**:
   ```bash
   # Проверка HTTP ответа
   curl -I http://smtu-med.ru
   curl -I http://www.smtu-med.ru

   # Проверка WebSocket
   # Установка wscat если нужно
   npm install -g wscat
   wscat -c ws://smtu-med.ru/ws/queue/
   ```

## Обслуживание

1. **Мониторинг ресурсов**:
   ```bash
   # Мониторинг использования ресурсов контейнерами
   docker stats

   # Проверка места на диске
   df -h /var/www/med_center
   
   # Мониторинг логов в реальном времени
   tail -f logs/django.log
   tail -f docker_compose/nginx/logs/access.log
   tail -f docker_compose/nginx/logs/error.log
   ```

2. **Управление сервисами**:
   ```bash
   # Перезапуск всех сервисов
   make prod-down
   make app-prod

   # Перезапуск отдельного сервиса
   docker-compose -f docker_compose/docker-compose.prod.yaml restart nginx
   ```

3. **Обновление приложения**:
   ```bash
   # Создание резервной копии
   tar -czf backup-$(date +%Y%m%d).tar.gz static media .env.prod

   # Обновление кода
   git pull

   # Перезапуск с новой версией
   ./deploy.sh
   ```

## Решение проблем

1. **Проверка системных требований**:
   ```bash
   # Проверка памяти
   free -h
   
   # Проверка процессора
   nproc
   lscpu
   
   # Проверка диска
   df -h
   ```

2. **Проблемы с сетью**:
   ```bash
   # Проверка портов
   sudo netstat -tulpn | grep -E ':(80|443|8000)'
   
   # Проверка DNS
   dig smtu-med.ru
   host smtu-med.ru
   
   # Проверка файрвола
   sudo ufw status
   sudo firewall-cmd --list-all
   ```

3. **Проблемы с Docker**:
   ```bash
   # Проверка статуса Docker
   systemctl status docker
   
   # Очистка неиспользуемых ресурсов
   docker system prune -a
   
   # Проверка логов Docker
   journalctl -u docker
   ```

## Рекомендации по безопасности

1. **Регулярные обновления**:
   ```bash
   # Обновление системы
   sudo apt update && sudo apt upgrade -y
   
   # Обновление Docker образов
   docker-compose -f docker_compose/docker-compose.prod.yaml pull
   ```

2. **Бэкапы**:
   ```bash
   # Бэкап базы данных
   docker exec medcenter-db pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql
   
   # Бэкап медиа файлов
   tar -czf media-backup.tar.gz media/
   ```

3. **Мониторинг безопасности**:
   ```bash
   # Проверка открытых портов
   sudo nmap -sT -p- localhost
   
   # Проверка прав файлов
   find /var/www/med_center -type f -ls
   ``` 