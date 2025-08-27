# 🔒 Инструкция по настройке HTTPS для продакшена

## 🚀 Быстрое переключение режимов

**Для быстрого переключения между режимами разработки и продакшена используйте:**
```bash
./switch_mode.sh
```

Этот скрипт предоставляет интерактивное меню для:
- 🏠 Переключения в режим локальной разработки (localhost:8080)
- 🔒 Переключения в продакшен режим с HTTPS
- 📖 Просмотра инструкции по HTTPS
- ℹ️ Получения информации о текущем режиме

---

## 📋 Обзор системы

Проект настроен для автоматического обновления SSL сертификатов Let's Encrypt через Certbot.

### Компоненты:
- **Certbot** - автоматическое обновление сертификатов
- **Nginx** - веб-сервер с SSL поддержкой
- **Let's Encrypt** - бесплатные SSL сертификаты

---

## 🚀 Пошаговая настройка HTTPS

### ⚡ Автоматическое переключение (рекомендуется)
```bash
# Переключение в продакшен режим
./switch_to_production.sh

# Переключение в режим разработки
./switch_to_development.sh

# Интерактивное меню
./switch_mode.sh
```

### 📝 Ручная настройка

#### Шаг 1: Восстановление Nginx конфигурации

Замените содержимое файла `nginx/default.conf` на оригинальную конфигурацию:

```nginx
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
```

### Шаг 2: Восстановление Django HTTPS настроек

В файле `django-backend/src/proj/settings.py` раскомментируйте HTTPS настройки:

```python
# HTTPS настройки для продакшена
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Отключите DEBUG для продакшена
DEBUG = False

# Убедитесь, что домен указан правильно
ALLOWED_HOSTS = ['queen-cosmo.ru', 'www.queen-cosmo.ru']
```

### Шаг 3: Восстановление Docker Compose портов

В файле `docker-compose.yml` добавьте HTTPS порт для Nginx:

```yaml
nginx:
  restart: always
  build:
      context: ./nginx
  ports:
      - "80:80"      # HTTP
      - "443:443"    # HTTPS
  volumes:
      - ./persistentdata/certbot/conf:/etc/letsencrypt
      - ./persistentdata/certbot/www:/var/www/certbot
      - ./persistentdata/static:/var/www/static
      - ./persistentdata/media:/var/www/media
      - ./persistentdata/robots.txt:/var/www/robots.txt
      - ./persistentdata/favicon.svg:/var/www/favicon.svg
```

### Шаг 4: Запуск сервисов

```bash
# Остановите текущие сервисы
docker-compose down

# Запустите все сервисы включая certbot
docker-compose up -d

# Проверьте статус
docker-compose ps
```

---

## 🔐 Первоначальная настройка SSL сертификатов

### Если сертификаты еще не получены:

1. **Остановите Nginx:**
```bash
docker-compose stop nginx
```

2. **Получите первый сертификат:**
```bash
docker-compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot \
  --email your-email@example.com \
  --agree-tos --no-eff-email \
  -d queen-cosmo.ru -d www.queen-cosmo.ru
```

3. **Запустите Nginx:**
```bash
docker-compose up nginx -d
```

---

## 🔄 Автоматическое обновление

Certbot автоматически обновляет сертификаты каждые 12 часов:

```yaml
certbot:
  entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

### Проверка обновления:
```bash
# Посмотреть логи certbot
docker-compose logs certbot

# Принудительное обновление (тест)
docker-compose exec certbot certbot renew --dry-run
```

---

## 🧪 Тестирование

### Проверка HTTP -> HTTPS редиректа:
```bash
curl -I http://queen-cosmo.ru
# Должен вернуть 301 редирект на https://
```

### Проверка SSL сертификата:
```bash
curl -I https://queen-cosmo.ru
# Должен вернуть 200 OK с SSL
```

### Проверка Let's Encrypt challenge:
```bash
curl http://queen-cosmo.ru/.well-known/acme-challenge/
# Должен вернуть содержимое папки certbot
```

---

## 🚨 Устранение неполадок

### Проблема: Сертификат не обновляется
```bash
# Проверьте логи
docker-compose logs certbot

# Проверьте права доступа к папкам
ls -la persistentdata/certbot/
```

### Проблема: Nginx не запускается
```bash
# Проверьте конфигурацию
docker-compose exec nginx nginx -t

# Проверьте логи
docker-compose logs nginx
```

### Проблема: Django не работает по HTTPS
```bash
# Проверьте настройки Django
docker-compose exec django-backend python src/manage.py check --deploy
```

---

## 📝 Важные замечания

1. **Домен должен указывать на ваш сервер** (DNS настройки)
2. **Порт 80 и 443 должны быть открыты** в файрволле
3. **Let's Encrypt имеет лимиты** - не более 50 сертификатов в неделю
4. **Сертификаты действительны 90 дней** - обновление происходит автоматически

---

## 🔄 Откат к localhost

Если нужно вернуться к локальной разработке:

### ⚡ Автоматический откат (рекомендуется)
```bash
./switch_to_development.sh
```

### 📝 Ручной откат

1. **Восстановите localhost конфигурацию Nginx**
2. **Отключите HTTPS в Django settings**
3. **Измените порты в docker-compose.yml**
4. **Перезапустите сервисы**

---

## 📞 Поддержка

### 🚀 Быстрые решения
```bash
# Проверить текущий режим
./switch_mode.sh

# Переключиться в другой режим
./switch_to_production.sh    # или
./switch_to_development.sh
```

### 🔍 Диагностика проблем

При возникновении проблем:
1. Проверьте логи: `docker-compose logs [service_name]`
2. Убедитесь, что домен правильно настроен
3. Проверьте права доступа к папкам certbot
4. Убедитесь, что порты 80 и 443 открыты
