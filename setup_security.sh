#!/bin/bash

echo "🔒 Настройка безопасности проекта Queen Cosmo"
echo "=============================================="

# Проверяем, что мы в корневой папке проекта
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Ошибка: Запустите скрипт из корневой папки проекта"
    exit 1
fi

echo "📋 Шаг 1: Генерация новых секретных ключей..."
python3 generate_secrets.py

echo ""
echo "📋 Шаг 2: Создание конфиденциальных файлов..."

# Создаем locals_vars.py из шаблона
if [ ! -f "django-backend/src/proj/locals_vars.py" ]; then
    echo "   Создаю locals_vars.py из шаблона..."
    cp django-backend/src/proj/locals_vars.py.example django-backend/src/proj/locals_vars.py
    echo "   ⚠️  ВАЖНО: Отредактируйте locals_vars.py и замените placeholder'ы!"
else
    echo "   ⚠️  locals_vars.py уже существует. Проверьте его содержимое!"
fi

# Создаем .pg-env из шаблона
if [ ! -f "postgresql-db/.pg-env" ]; then
    echo "   Создаю .pg-env из шаблона..."
    cp postgresql-db/.pg-env.example postgresql-db/.pg-env
    echo "   ⚠️  ВАЖНО: Отредактируйте .pg-env и замените placeholder'ы!"
else
    echo "   ⚠️  .pg-env уже существует. Проверьте его содержимое!"
fi

echo ""
echo "📋 Шаг 3: Проверка .gitignore..."
if grep -q "locals_vars.py" .gitignore && grep -q ".pg-env" .gitignore; then
    echo "   ✅ .gitignore настроен правильно"
else
    echo "   ❌ .gitignore настроен неправильно!"
fi

echo ""
echo "📋 Шаг 4: Удаление конфиденциальных файлов из Git..."
echo "   Удаляю locals_vars.py из Git (файл останется локально)..."
git rm --cached django-backend/src/proj/locals_vars.py 2>/dev/null || echo "   Файл не был в Git"

echo "   Удаляю .pg-env из Git (файл останется локально)..."
git rm --cached postgresql-db/.pg-env 2>/dev/null || echo "   Файл не был в Git"

echo ""
echo "🔐 Настройка безопасности завершена!"
echo ""
echo "📝 СЛЕДУЮЩИЕ ШАГИ:"
echo "1. Отредактируйте django-backend/src/proj/locals_vars.py"
echo "2. Отредактируйте postgresql-db/.pg-env"
echo "3. Замените placeholder'ы на реальные значения"
echo "4. Перезапустите Docker контейнеры"
echo "5. Создайте суперпользователя Django"
echo ""
echo "⚠️  ВАЖНО: НИКОГДА не коммитьте конфиденциальные файлы в Git!"
echo "   Они уже добавлены в .gitignore"
