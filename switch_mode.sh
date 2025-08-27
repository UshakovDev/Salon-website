#!/bin/bash

# 🔄 Скрипт переключения режимов работы проекта
# Использование: ./switch_mode.sh

echo "🔄 Переключение режимов работы проекта Salon-website"
echo "=================================================="
echo ""

# Проверяем текущий режим
if grep -q "localhost 127.0.0.1" nginx/default.conf; then
    CURRENT_MODE="🏠 Локальная разработка (localhost:8080)"
else
    CURRENT_MODE="🔒 Продакшен (HTTPS)"
fi

echo "📍 Текущий режим: $CURRENT_MODE"
echo ""

echo "Выберите режим работы:"
echo "1) 🏠 Переключиться в режим локальной разработки"
echo "2) 🔒 Переключиться в продакшен режим с HTTPS"
echo "3) 📖 Показать инструкцию по HTTPS"
echo "4) ℹ️  Информация о текущем режиме"
echo "5) ❌ Выход"
echo ""

read -p "Введите номер (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🏠 Переключение в режим локальной разработки..."
        ./switch_to_development.sh
        ;;
    2)
        echo ""
        echo "🔒 Переключение в продакшен режим..."
        ./switch_to_production.sh
        ;;
    3)
        echo ""
        echo "📖 Инструкция по настройке HTTPS:"
        echo "=================================="
        cat HTTPS_SETUP.md
        ;;
    4)
        echo ""
        echo "ℹ️  Информация о текущем режиме:"
        echo "================================="
        echo "📍 Режим: $CURRENT_MODE"
        echo ""
        echo "🌐 Доступные адреса:"
        if grep -q "localhost 127.0.0.1" nginx/default.conf; then
            echo "   - http://localhost:8080 (основной)"
            echo "   - http://127.0.0.1:8080"
        else
            echo "   - https://queen-cosmo.ru (основной)"
            echo "   - http://queen-cosmo.ru (редирект на HTTPS)"
        fi
        echo ""
        echo "🔧 Порт Nginx:"
        if grep -q "8080:80" docker-compose.yml; then
            echo "   - 8080:80 (localhost режим)"
        else
            echo "   - 80:80 и 443:443 (продакшен режим)"
        fi
        echo ""
        echo "🐍 Django DEBUG:"
        if grep -q "DEBUG = True" django-backend/src/proj/settings.py; then
            echo "   - Включен (режим разработки)"
        else
            echo "   - Отключен (продакшен режим)"
        fi
        ;;
    5)
        echo "👋 До свидания!"
        exit 0
        ;;
    *)
        echo "❌ Неверный выбор. Попробуйте снова."
        exit 1
        ;;
esac

echo ""
echo "✅ Операция завершена!"
echo "🔄 Для применения изменений перезапустите сервисы:"
echo "   docker-compose down && docker-compose up -d"
