FROM mirror.gcr.io/library/python:3.11-alpine

# Устанавливаем системные зависимости
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Копируем requirements.txt для кеширования слоя pip
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src/ ./src/

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Запускаем Gunicorn
CMD ["gunicorn", "-w", "3", "--chdir", "./src", "proj.wsgi:application", "--bind", "0.0.0.0:8000"]
