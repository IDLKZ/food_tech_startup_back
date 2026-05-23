## Остановка и удаление записей
1. docker compose -f docker-compose.dev.yml down -v
## Вновь запуск сервисов докер
1. docker compose -f docker-compose.dev.yml up -d


### Миграции алембик + репликация
### Команда	Описание
- uv lock	Создает/обновляет uv.lock на основе pyproject.toml.
- uv sync	Синхронизирует виртуальное окружение с uv.lock.
- uv sync --no-dev	Устанавливает только основные зависимости (без тестовых/dev-инструментов).
- uv add package	Добавляет пакет в проект и обновляет зависимости.


## Новая миграция
1. uv run alembic revision --autogenerate -m "название"
2. uv run alembic upgrade head
3. $env:DATABASE_SYNC_URL="postgresql+psycopg://food_tech:food_tech_pass@localhost:5434/food_tech"
   uv run alembic upgrade head
   $env:DATABASE_SYNC_URL="postgresql+psycopg://food_tech:food_tech_pass@localhost:5433/food_tech"

## Репликация — полный сброс (если контейнеры пересоздавались)
1. docker exec -it food_tech_postgres_primary psql -U food_tech -d food_tech -c "
   CREATE USER replicator WITH REPLICATION PASSWORD 'rep_secret';
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO replicator;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO replicator;
   CREATE PUBLICATION food_tech_pub FOR ALL TABLES;"

2. docker exec -it food_tech_postgres_replica psql -U food_tech -d food_tech -c "
   DROP SUBSCRIPTION IF EXISTS food_tech_sub;
   CREATE SUBSCRIPTION food_tech_sub
   CONNECTION 'host=postgres-primary port=5432 dbname=food_tech user=replicator password=rep_secret'
   PUBLICATION food_tech_pub;"

## Проверка репликации
docker exec -it food_tech_postgres_primary psql -U food_tech -d food_tech -c "SELECT * FROM pg_stat_replication;"
docker exec -it food_tech_postgres_replica psql -U food_tech -d food_tech -c "SELECT * FROM pg_stat_subscription;"


### Автоперевод Babel
# компилируем все языки
pybabel compile -d app/core/locales -D messages

# 1. создать .po файлы из кода (если используешь _() маркеры)
pybabel extract -F babel.cfg -o app/core/locales/messages.pot .

# 2. обновить существующие .po файлы
pybabel update -i app/core/locales/messages.pot -d app/locales -D messages

# 3. скомпилировать .po → .mo (обязательно перед запуском)
pybabel compile -d app/core/locales -D messages

# 4.После добавления новых переводов в .po файлы:
pybabel compile -d app/core/locales -D messages