#!/usr/bin/env python3
"""
Скрипт для генерации новых секретных ключей и паролей
Используйте этот скрипт для создания безопасных ключей
"""

import secrets
import string
import os

def generate_secret_key(length=50):
    """Генерирует Django SECRET_KEY"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_password(length=16):
    """Генерирует безопасный пароль"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Убираем похожие символы
    alphabet = alphabet.replace('0', '').replace('O', '').replace('1', '').replace('l', '')
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("🔐 Генерация новых секретных ключей")
    print("=" * 50)
    
    # Генерируем Django SECRET_KEY
    django_secret = generate_secret_key()
    print(f"🔑 Django SECRET_KEY:")
    print(f"   {django_secret}")
    print()
    
    # Генерируем пароль для PostgreSQL
    db_password = generate_password()
    print(f"🗄️  PostgreSQL пароль:")
    print(f"   {db_password}")
    print()
    
    # Генерируем пароль для админки Django
    admin_password = generate_password()
    print(f"👤 Django Admin пароль:")
    print(f"   {admin_password}")
    print()
    
    print("📝 Инструкции:")
    print("1. Скопируйте django-backend/src/proj/locals_vars.py.example в locals_vars.py")
    print("2. Замените placeholder'ы на сгенерированные значения")
    print("3. Скопируйте postgresql-db/.pg-env.example в .pg-env")
    print("4. Замените пароль PostgreSQL")
    print("5. Создайте суперпользователя Django с новым паролем")
    print()
    print("⚠️  ВАЖНО: НИКОГДА не коммитьте locals_vars.py и .pg-env в Git!")
    print("   Эти файлы уже добавлены в .gitignore")

if __name__ == "__main__":
    main()
