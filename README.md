# 🎨 Queen Cosmo - Салон красоты

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue.svg)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/Nginx-✓-green.svg)](https://nginx.org/)
[![Security](https://img.shields.io/badge/Security-🔒-red.svg)](SECURITY_README.md)

> **Современный веб-сайт салона красоты "Queen Cosmo" с полной автоматизацией и безопасностью**

## 🌟 **Особенности проекта**

- 🎯 **Полнофункциональный сайт** салона красоты
- 🐳 **Docker контейнеризация** для простого развертывания
- 🔒 **Полная безопасность** с защитой конфиденциальных данных
- 📱 **Адаптивный дизайн** для всех устройств
- 🚀 **Автоматическая настройка** и заполнение тестовыми данными
- 🎨 **Современный UI/UX** с анимациями и интерактивностью
- 📊 **SEO оптимизация** с мета-тегами и микроразметкой
- 🔄 **Горячая перезагрузка** для разработки

## 🏗️ **Архитектура**

```
Salon-website/
├── 🐍 django-backend/          # Django 4.2.7 приложение
├── 🌐 nginx/                   # Веб-сервер Nginx
├── 🗄️  postgresql-db/           # База данных PostgreSQL
├── 💾 persistentdata/          # Постоянные данные
├── 🔒 security/                # Файлы безопасности
└── 🐳 docker-compose.yml       # Оркестрация сервисов
```

## 🚀 **Быстрый старт**

### **1. Клонирование проекта**
```bash
git clone https://github.com/UshakovDev/Salon-website.git
cd Salon-website
```

### **2. Запуск всех сервисов**
```bash
# Запустить все контейнеры
docker-compose up -d

# Проверить статус
docker-compose ps
```

### **3. Заполнение тестовыми данными**
```bash
# Автоматическое заполнение сайта
docker-compose exec django-backend python src/manage.py fill_test_data
```

### **4. Открыть сайт**
```
🌐 http://localhost:8080
```

## 🛠️ **Технологический стек**

### **Backend**
- **Django 4.2.7** - веб-фреймворк
- **PostgreSQL** - база данных
- **Gunicorn** - WSGI сервер
- **Python 3.11** - язык программирования

### **Frontend**
- **HTML5** - семантическая разметка
- **CSS3** - стили и анимации
- **JavaScript** - интерактивность
- **Responsive Design** - адаптивность

### **DevOps**
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация
- **Nginx** - веб-сервер
- **Let's Encrypt** - SSL сертификаты

### **Безопасность**
- **CSRF защита** - защита от атак
- **Кеширование** - оптимизация производительности
- **Валидация данных** - безопасность ввода
- **Защищенные переменные** - конфиденциальность

## 📱 **Функциональность сайта**

### **Главная страница**
- 🏠 **Приветствие** - описание студии
- ✨ **Почему выбирают нас** - преимущества
- 👩‍🎨 **О нас** - информация о Queen Cosmo
- 🛍️ **Каталог услуг** - категории и подкатегории
- 💰 **Прайс-лист** - цены на услуги
- 🖼️ **Галерея работ** - 3D слайдер фотографий
- 📍 **Контакты** - адрес и карта

### **Дополнительные страницы**
- 🏆 **Сертификаты** - достижения специалистов
- 🔒 **Политика конфиденциальности** - правовая информация

## 🎨 **Дизайн и UX**

- **Современный интерфейс** с золотыми акцентами
- **Плавные анимации** и переходы
- **Интерактивная галерея** с 3D эффектами
- **Адаптивное меню** для мобильных устройств
- **Оптимизированные изображения** для быстрой загрузки
- **Семантическая разметка** для SEO

## 🔒 **Безопасность**

Проект полностью защищен от утечек конфиденциальной информации:

- ✅ **Django SECRET_KEY** - защищен от попадания в Git
- ✅ **Пароли БД** - защищены от попадания в Git
- ✅ **Переменные окружения** - защищены от попадания в Git
- ✅ **Автоматическая генерация** безопасных ключей
- ✅ **Полная документация** по безопасности

📖 **[Подробнее о безопасности →](SECURITY_README.md)**

## 📊 **Модели данных**

### **Контент**
- `Immutable_content` - неизменяемый контент
- `SiteContent` - мета-теги для SEO

### **Услуги и цены**
- `Category` - категории услуг
- `Subcategory` - подкатегории услуг
- `PriceList` - прайс-лист

### **Медиа**
- `ImageCategory` - категории фотографий
- `Image` - фотографии работ
- `Certificates` - сертификаты

### **Правовая информация**
- `PrivacyPolicy` - политика конфиденциальности
- `DataCollection` - сбор данных
- `ThirdPartyDataTransfer` - передача данных

## 🚀 **Команды Django**

### **Автоматизация контента**
```bash
# Заполнить тестовыми данными
python src/manage.py fill_test_data

# Очистить тестовые данные
python src/manage.py clear_test_data

# Тестирование CSRF защиты
python src/manage.py test_csrf
```

### **Управление проектом**
```bash
# Создать суперпользователя
python src/manage.py createsuperuser

# Запустить shell
python src/manage.py shell

# Проверить миграции
python src/manage.py showmigrations
```

## 🔧 **Настройка и конфигурация**

### **Переменные окружения**
Проект использует безопасную систему переменных:

1. **Скопировать шаблоны:**
   ```bash
   cp django-backend/src/proj/locals_vars.py.example django-backend/src/proj/locals_vars.py
   cp postgresql-db/.pg-env.example postgresql-db/.pg-env
   ```

2. **Отредактировать файлы** и заменить placeholder'ы
3. **Перезапустить контейнеры**

### **Автоматическая настройка безопасности**
```bash
# Запустить скрипт настройки
./setup_security.sh

# Сгенерировать новые ключи
python3 generate_secrets.py
```

## 📱 **Адаптивность**

Сайт полностью адаптирован для всех устройств:

- **Desktop** (1200px+) - полная функциональность
- **Tablet** (768px-1199px) - адаптированный интерфейс
- **Mobile** (до 767px) - мобильная версия
- **Touch-friendly** - оптимизация для сенсорных экранов

## 🌐 **SEO и аналитика**

- **Мета-теги** для всех страниц
- **Open Graph** разметка для соцсетей
- **Schema.org** микроразметка
- **Яндекс.Метрика** интеграция
- **Оптимизированные URL** и структура
- **Sitemap** готовность

## 🚀 **Режимы работы**

### **Режим разработки**
```bash
./switch_to_development.sh
# http://localhost:8080
```

### **Режим продакшена**
```bash
./switch_to_production.sh
# https://queen-cosmo.ru
```

### **Интерактивное меню**
```bash
./switch_mode.sh
```

## 📚 **Документация проекта**

### **📖 Основная документация**
- **[README.md](README.md)** - этот файл, обзор проекта
- **[QUICK_START.md](QUICK_START.md)** - быстрый старт и настройка
- **[SECURITY_README.md](SECURITY_README.md)** - полная документация по безопасности

### **🔧 Техническая документация**
- **[TEST_DATA_README.md](TEST_DATA_README.md)** - заполнение тестовыми данными
- **[HTTPS_SETUP.md](HTTPS_SETUP.md)** - настройка HTTPS и SSL сертификатов
- **[docker-compose.yml](docker-compose.yml)** - конфигурация Docker сервисов

### **🐳 Docker документация**
- **[django-backend/Dockerfile](django-backend/Dockerfile)** - образ Django приложения
- **[nginx/Dockerfile](nginx/Dockerfile)** - образ Nginx сервера
- **[django-backend/requirements.txt](django-backend/requirements.txt)** - Python зависимости

### **⚙️ Конфигурационные файлы**
- **[django-backend/src/proj/settings.py](django-backend/src/proj/settings.py)** - настройки Django
- **[nginx/default.conf](nginx/default.conf)** - конфигурация Nginx
- **[.gitignore](.gitignore)** - Git исключения

### **🔐 Скрипты безопасности**
- **[generate_secrets.py](generate_secrets.py)** - генератор безопасных ключей
- **[setup_security.sh](setup_security.sh)** - автоматическая настройка безопасности

### **🚀 Скрипты развертывания**
- **[switch_mode.sh](switch_mode.sh)** - интерактивное переключение режимов
- **[switch_to_development.sh](switch_to_development.sh)** - режим разработки
- **[switch_to_production.sh](switch_to_production.sh)** - режим продакшена

## 📁 **Структура проекта**

```
Salon-website/
├── 📖 README.md                    # Этот файл
├── 🔒 SECURITY_README.md           # Документация по безопасности
├── 🚀 QUICK_START.md               # Быстрый старт
├── 📝 TEST_DATA_README.md          # Заполнение тестовыми данными
├── 🌐 HTTPS_SETUP.md               # Настройка HTTPS
├── 🐳 docker-compose.yml           # Docker конфигурация
├── 🐍 django-backend/              # Django приложение
│   ├── 📁 src/                     # Исходный код
│   │   ├── 📁 proj/                # Настройки проекта
│   │   │   ├── ⚙️  settings.py      # Конфигурация Django
│   │   │   ├── 🌐 urls.py          # URL маршруты
│   │   │   └── 🔐 locals_vars.py   # Переменные окружения
│   │   ├── 📁 saloon/              # Основное приложение
│   │   │   ├── 📊 models.py        # Модели данных
│   │   │   ├── 🎯 views.py         # Представления
│   │   │   ├── 🌐 urls.py          # URL приложения
│   │   │   ├── 👨‍💼 admin.py        # Админ-панель
│   │   │   ├── 🎨 templates/       # HTML шаблоны
│   │   │   ├── 🎨 static/          # CSS, JS, изображения
│   │   │   └── 🔧 management/      # Команды Django
│   │   └── 🐍 manage.py            # Управление Django
│   ├── 🐳 Dockerfile               # Docker образ Django
│   └── 📋 requirements.txt         # Python зависимости
├── 🌐 nginx/                       # Веб-сервер
│   ├── 🐳 Dockerfile               # Docker образ Nginx
│   └── ⚙️  default.conf             # Конфигурация Nginx
├── 🗄️  postgresql-db/               # База данных
│   └── 🔐 .pg-env                  # Переменные PostgreSQL
├── 💾 persistentdata/              # Постоянные данные
│   ├── 🗄️  db/                     # База данных
│   ├── 📁 static/                  # Статические файлы
│   ├── 📁 media/                    # Медиа файлы
│   └── 🔐 queen_cosmo_cache/       # Кеш Django
├── 🔐 generate_secrets.py          # Генератор ключей
├── 🛡️  setup_security.sh           # Настройка безопасности
└── 📁 .gitignore                   # Git исключения
```

## 🆘 **Решение проблем**

### **Сайт не загружается**
```bash
# Проверить статус сервисов
docker-compose ps

# Проверить логи
docker-compose logs django-backend
docker-compose logs nginx
```

### **Данные не отображаются**
```bash
# Заполнить тестовыми данными
docker-compose exec django-backend python src/manage.py fill_test_data

# Проверить базу данных
docker-compose exec django-backend python src/manage.py shell
```

### **Проблемы с безопасностью**
```bash
# Запустить настройку безопасности
./setup_security.sh

# Проверить .gitignore
cat .gitignore | grep -E "(locals_vars|\.pg-env|\.env)"
```

## 🤝 **Вклад в проект**

1. **Fork** репозитория
2. **Создать** feature ветку (`git checkout -b feature/AmazingFeature`)
3. **Сделать** коммит (`git commit -m 'Add some AmazingFeature'`)
4. **Push** в ветку (`git push origin feature/AmazingFeature`)
5. **Создать** Pull Request

## 📄 **Лицензия**

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.
