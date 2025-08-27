# 🔒 Руководство по безопасности проекта Queen Cosmo

## ⚠️ **КРИТИЧЕСКИ ВАЖНО**

Этот проект содержит конфиденциальную информацию, которая **НИКОГДА** не должна попадать в Git!

## 🚨 **Обнаруженные проблемы безопасности**

### **1. Django SECRET_KEY в Git**
- **Файл**: `django-backend/src/proj/locals_vars.py`
- **Проблема**: Содержит реальный SECRET_KEY
- **Риск**: Компрометация сессий, CSRF токенов

### **2. Пароли PostgreSQL в Git**
- **Файл**: `postgresql-db/.pg-env`
- **Проблема**: Содержит реальные пароли БД
- **Риск**: Доступ к базе данных

## ✅ **Что исправлено**

### **1. Обновлен .gitignore**
Добавлены правила для защиты:
```
# КРИТИЧЕСКИ ВАЖНО: Конфиденциальные файлы
locals_vars.py
*.env
.env
.env.local
.env.production
.env.development
.pg-env
postgresql-db/.pg-env

# Дополнительные файлы безопасности
*.key
*.pem
*.crt
*.p12
*.pfx
secrets.json
secrets.yaml
secrets.yml
config.json
config.yaml
config.yml
```

### **2. Созданы шаблоны файлов**
- `locals_vars.py.example` - шаблон для Django переменных
- `.pg-env.example` - шаблон для PostgreSQL переменных
- `.env.example` - общий шаблон переменных

### **3. Созданы скрипты безопасности**
- `generate_secrets.py` - генерация новых ключей
- `setup_security.sh` - автоматическая настройка безопасности

## 🔐 **Как настроить безопасность**

### **Автоматическая настройка:**
```bash
# Запустить скрипт настройки безопасности
./setup_security.sh
```

### **Ручная настройка:**
```bash
# 1. Сгенерировать новые ключи
python3 generate_secrets.py

# 2. Создать конфиденциальные файлы из шаблонов
cp django-backend/src/proj/locals_vars.py.example django-backend/src/proj/locals_vars.py
cp postgresql-db/.pg-env.example postgresql-db/.pg-env

# 3. Отредактировать файлы и заменить placeholder'ы
nano django-backend/src/proj/locals_vars.py
nano postgresql-db/.pg-env

# 4. Удалить файлы из Git (но оставить локально)
git rm --cached django-backend/src/proj/locals_vars.py
git rm --cached postgresql-db/.pg-env
```

## 📁 **Структура файлов безопасности**

```
Salon-website/
├── .gitignore                    # ✅ Защищает конфиденциальные файлы
├── locals_vars.py.example        # ✅ Шаблон Django переменных
├── .pg-env.example              # ✅ Шаблон PostgreSQL переменных
├── .env.example                  # ✅ Общий шаблон переменных
├── generate_secrets.py           # ✅ Генератор ключей
├── setup_security.sh             # ✅ Скрипт настройки
├── SECURITY_README.md            # ✅ Эта документация
├── django-backend/src/proj/
│   ├── locals_vars.py           # ❌ В .gitignore (конфиденциальный)
│   └── locals_vars.py.example   # ✅ В Git (шаблон)
└── postgresql-db/
    ├── .pg-env                   # ❌ В .gitignore (конфиденциальный)
    └── .pg-env.example           # ✅ В Git (шаблон)
```

## 🔑 **Переменные, которые нужно настроить**

### **Django (locals_vars.py):**
```python
SECRET_KEY = 'ВАШ_НОВЫЙ_SECRET_KEY_ЗДЕСЬ'
PG_NAME = 'queen_cosmo_db'
PG_USER = 'queen_cosmo_user'
PG_PASSWORD = 'ВАШ_РЕАЛЬНЫЙ_ПАРОЛЬ_ЗДЕСЬ'
PG_HOST = 'postgresql-db'
PG_PORT = '5432'
```

### **PostgreSQL (.pg-env):**
```bash
POSTGRES_DB=queen_cosmo_db
POSTGRES_USER=queen_cosmo_user
POSTGRES_PASSWORD=ВАШ_РЕАЛЬНЫЙ_ПАРОЛЬ_ЗДЕСЬ
POSTGRES_HOST=postgresql-db
POSTGRES_PORT=5432
```

## 🚀 **После настройки безопасности**

### **1. Перезапустить Docker контейнеры:**
```bash
docker-compose down
docker-compose up -d
```

### **2. Создать суперпользователя Django:**
```bash
docker-compose exec django-backend python src/manage.py createsuperuser
```

### **3. Проверить работу сайта:**
```bash
# Открыть в браузере
http://localhost:8080
```

## 🛡️ **Дополнительные меры безопасности**

### **1. Регулярная смена паролей**
- Django SECRET_KEY - каждые 3 месяца
- PostgreSQL пароли - каждые 6 месяцев
- Django Admin пароли - каждые 3 месяца

### **2. Мониторинг безопасности**
- Проверять логи на подозрительную активность
- Мониторить доступы к базе данных
- Отслеживать попытки взлома

### **3. Резервное копирование**
- Регулярно делать бэкапы базы данных
- Хранить конфиденциальные файлы в безопасном месте
- Использовать шифрование для бэкапов

## 🆘 **Что делать при компрометации**

### **1. Немедленные действия:**
- Сменить все пароли
- Сгенерировать новый Django SECRET_KEY
- Проверить логи на подозрительную активность
- Остановить все сервисы

### **2. Анализ инцидента:**
- Определить источник взлома
- Оценить масштаб ущерба
- Документировать все действия

### **3. Восстановление:**
- Восстановить из чистого бэкапа
- Настроить новую безопасность
- Провести тестирование

## 📞 **Поддержка по безопасности**

При возникновении проблем:
1. Проверьте эту документацию
2. Запустите `./setup_security.sh`
3. Проверьте настройки .gitignore
4. Убедитесь, что конфиденциальные файлы не в Git

---

**🔒 Безопасность - это не опция, а необходимость!**
