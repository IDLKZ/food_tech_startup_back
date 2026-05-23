# Используем slim версию для экономии места
FROM python:3.12-slim-bookworm

# Установка системных зависимостей для работы с БД
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --no-dev

# Копируем исходный код
COPY . .

# Запуск приложения
CMD ["python", "-m", "app.main"]