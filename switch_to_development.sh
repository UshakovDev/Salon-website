#!/bin/bash

# 🏠 Скрипт переключения в режим локальной разработки
# Использование: ./switch_to_development.sh

echo "🏠 Переключение в режим локальной разработки..."

# Шаг 1: Восстановление Nginx конфигурации для localhost
echo "📝 Восстанавливаю Nginx конфигурацию для localhost..."
cat > nginx/default.conf << 'EOF'
upstream innerdjango {
    server django-backend:8000;
}

server {
    listen 80;
    server_name localhost 127.0.0.1 queen-cosmo.ru www.queen-cosmo.ru;

    location / {
        proxy_set_header Host $host;
        proxy_pass http://innerdjango;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        root /var/www;
    }
    
    location /media/ {
        alias /var/www/media/;
    }
    
    location /robots.txt {
        alias /var/www/robots.txt;
    }
    
    location /favicon.svg {
        alias /var/www/favicon.svg;
    }
}
EOF

# Шаг 2: Отключение Django HTTPS настроек
echo "🐍 Отключаю Django HTTPS настройки..."
sed -i 's/^SECURE_PROXY_SSL_HEADER/# SECURE_PROXY_SSL_HEADER/g' django-backend/src/proj/settings.py
sed -i 's/^SECURE_SSL_REDIRECT/# SECURE_SSL_REDIRECT/g' django-backend/src/proj/settings.py
sed -i 's/^SESSION_COOKIE_SECURE/# SESSION_COOKIE_SECURE/g' django-backend/src/proj/settings.py
sed -i 's/^CSRF_COOKIE_SECURE/# CSRF_COOKIE_SECURE/g' django-backend/src/proj/settings.py
sed -i 's/DEBUG = False/DEBUG = True/g' django-backend/src/proj/settings.py

# Шаг 3: Восстановление Docker Compose портов для localhost
echo "🐳 Восстанавливаю Docker Compose порты для localhost..."
sed -i 's/- "80:80"/- "8080:80"/g' docker-compose.yml
sed -i '/- "443:443"/d' docker-compose.yml

echo "✅ Конфигурация восстановлена для локальной разработки!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Перезапустите сервисы: docker-compose down && docker-compose up -d"
echo "2. Сайт будет доступен по адресу: http://localhost:8080"
echo "3. Статические файлы и Django будут работать в режиме отладки"
echo ""
echo "🔄 Для возврата в продакшен используйте: ./switch_to_production.sh"
echo "📖 Подробная инструкция: cat HTTPS_SETUP.md"
