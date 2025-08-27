#!/bin/bash

# 🔒 Скрипт переключения в продакшен режим с HTTPS
# Использование: ./switch_to_production.sh

echo "🚀 Переключение в продакшен режим с HTTPS..."

# Шаг 1: Восстановление Nginx конфигурации
echo "📝 Восстанавливаю Nginx конфигурацию для HTTPS..."
cat > nginx/default.conf << 'EOF'
upstream innerdjango {
    server django-backend:8000;
}

# HTTP сервер - редирект на HTTPS
server {
    listen 80;
    server_name queen-cosmo.ru www.queen-cosmo.ru;

    location / {
        return 301 https://$host$request_uri;
    }
    
    # Let's Encrypt challenge для проверки домена
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
}

# HTTPS сервер
server {
    listen 443 ssl;
    server_name queen-cosmo.ru;
    
    # SSL сертификаты
    ssl_certificate /etc/letsencrypt/live/queen-cosmo.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/queen-cosmo.ru/privkey.pem;
    
    # SSL настройки
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
    location / {
        proxy_set_header Host $host;
        proxy_pass http://innerdjango;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
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

# Шаг 2: Восстановление Django HTTPS настроек
echo "🐍 Восстанавливаю Django HTTPS настройки..."
sed -i 's/# SECURE_PROXY_SSL_HEADER/SECURE_PROXY_SSL_HEADER/g' django-backend/src/proj/settings.py
sed -i 's/# SECURE_SSL_REDIRECT/SECURE_SSL_REDIRECT/g' django-backend/src/proj/settings.py
sed -i 's/# SESSION_COOKIE_SECURE/SESSION_COOKIE_SECURE/g' django-backend/src/proj/settings.py
sed -i 's/# CSRF_COOKIE_SECURE/CSRF_COOKIE_SECURE/g' django-backend/src/proj/settings.py
sed -i 's/DEBUG = True/DEBUG = False/g' django-backend/src/proj/settings.py

# Шаг 3: Восстановление Docker Compose портов
echo "🐳 Восстанавливаю Docker Compose порты..."
sed -i 's/- "8080:80"/- "80:80"\n        - "443:443"/g' docker-compose.yml

echo "✅ Конфигурация восстановлена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Убедитесь, что домен queen-cosmo.ru указывает на ваш сервер"
echo "2. Откройте порты 80 и 443 в файрволле"
echo "3. Запустите: docker-compose up -d"
echo "4. Если сертификатов нет, выполните команду из HTTPS_SETUP.md"
echo ""
echo "📖 Подробная инструкция: cat HTTPS_SETUP.md"
