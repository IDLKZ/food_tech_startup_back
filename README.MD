# 🍽️ Food Tech Startup

Backend платформа для управления ресторанным бизнесом. Clean Architecture + DDD на FastAPI.

---

## 🏗️ Архитектура

```
Presentation  →  Application  →  Domain
Infrastructure  →  Application (реализует интерфейсы)
```

### Слои

| Слой | Описание |
|---|---|
| **Domain** | Entities, Value Objects, Domain Events, Repository interfaces |
| **Application** | Use Cases, Commands, DTOs, Filters |
| **Infrastructure** | SQLAlchemy models, Repository implementations, UoW |
| **Presentation** | FastAPI Controllers, Schemas, Dependencies |

### Модули

```
app/
├── core/                          # DI контейнер, конфиги, middleware, исключения
│   ├── config/                    # AppConfig, DatabaseSettings, JWTSettings...
│   ├── di/                        # Dependency Injector Container
│   ├── exceptions/                # AppException иерархия
│   ├── middleware/                # LocaleMiddleware
│   ├── locales/                   # Ключи локализации
│   └── response/                  # ApiCommonResponse
│
├── modules/
│   ├── iam/                       # Identity & Access Management
│   │   ├── domain/
│   │   │   ├── entities/          # RoleEntity, UserEntity...
│   │   │   ├── value_objects/     # Email, Phone, Password, RoleValue...
│   │   │   ├── events/            # RoleCreatedEvent...
│   │   │   ├── exceptions/        # RoleNotFoundException...
│   │   │   └── repositories/      # RoleRepo (ABC)
│   │   ├── application/
│   │   │   ├── use_cases/         # CreateRoleUseCase...
│   │   │   └── dtos/              # RoleFilterDTO...
│   │   ├── infrastructure/
│   │   │   ├── models/            # RoleModel, UserModel...
│   │   │   ├── repo_impl/         # RoleRepositoryImpl
│   │   │   └── filters/           # RoleFilterImpl
│   │   └── presentation/
│   │       ├── controllers/       # RoleController
│   │       ├── schemas/           # CreateRoleSchema, RoleResponseSchema
│   │       ├── dependencies/      # get_create_role_use_case...
│   │       └── filters/           # RoleQueryFilter
│   │
│   ├── catalog/                   # Блюда, модификаторы, техкарты
│   ├── orders/                    # Заказы, оплата, чеки
│   ├── inventory/                 # Склад, остатки
│   ├── promotions/                # Промокоды, бонусы, лояльность
│   └── notifications/             # Push, SMS, Email, OTP
│
└── shared/
    ├── domain/
    │   ├── base_repository.py     # BaseRepo[E] (ABC)
    │   ├── base_aggregate.py      # AggregateRoot
    │   └── domain_event.py        # DomainEvent
    └── infrastructure/
        ├── models/
        │   ├── base_model.py      # Base, UUIDBase, TimestampMixin, FullBase
        │   └── shared_model_columns.py  # SharedModelColumns
        ├── repo_impl/
        │   └── base_repo_impl.py  # BaseRepoImpl[T]
        ├── filter/
        │   └── base_filter.py     # BaseFilter[T]
        ├── uow/
        │   ├── abstract_uow.py    # BaseUoW (ABC)
        │   └── sql_alchemy_uow.py # SqlAlchemyUoW
        └── dto/
            └── pagination_result.py  # PaginationResult[T]
```

---

## 🗄️ База данных

### CQRS — два PostgreSQL

```
Write (primary) :5433  ←  INSERT / UPDATE / DELETE
Read  (replica) :5434  ←  SELECT
        ↑
   Logical replication
```

### IAM таблицы

| Таблица | Описание |
|---|---|
| `users` | Пользователи |
| `roles` | Роли |
| `permissions` | Права доступа |
| `role_permissions` | Связь ролей и прав |
| `user_roles` | Связь пользователей и ролей |
| `groups` | Группы пользователей |
| `user_groups` | Связь пользователей и групп |
| `organizations` | Организации |
| `user_organizations` | Связь пользователей и организаций |

---

## 🚀 Запуск

### Требования

- Python 3.12+
- Docker Desktop
- uv

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your/food_tech_startup
cd food_tech_startup
```

### 2. Установить зависимости

```bash
uv sync
```

### 3. Поднять инфраструктуру

```bash
docker compose -f docker-compose.dev.yml up -d
```

Поднимает:
- `postgres-primary` → `:5433`
- `postgres-replica` → `:5434`
- `redis` → `:6379`
- `rabbitmq` → `:5672` (Management UI → `:15672`)
- `pgadmin` → `:8888`

### 4. Настроить окружение

```bash
cp .env.example .env.dev
# заполни переменные
```

### 5. Применить миграции

```bash
# primary
uv run alembic upgrade head

# replica
$env:DATABASE_SYNC_URL="postgresql+psycopg://food_tech:food_tech_pass@localhost:5434/food_tech"
uv run alembic upgrade head
$env:DATABASE_SYNC_URL="postgresql+psycopg://food_tech:food_tech_pass@localhost:5433/food_tech"
```

### 6. Настроить репликацию (один раз)

```bash
# publication на primary
docker exec -it food_tech_postgres_primary psql -U food_tech -d food_tech -c "
CREATE USER replicator WITH REPLICATION PASSWORD 'rep_secret';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO replicator;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO replicator;
CREATE PUBLICATION food_tech_pub FOR ALL TABLES;"

# subscription на replica
docker exec -it food_tech_postgres_replica psql -U food_tech -d food_tech -c "
CREATE SUBSCRIPTION food_tech_sub
CONNECTION 'host=postgres-primary port=5432 dbname=food_tech user=replicator password=rep_secret'
PUBLICATION food_tech_pub;"
```

### 7. Запустить приложение

```bash
uv run python -m app.main
```

Swagger UI → `http://localhost:8000/docs`

---

## 🌐 Локализация

Поддерживаемые языки: **ru** (default), **kk**, **en**

```bash
# через query param
GET /api/v1/roles?lang=kk

# через заголовок
Accept-Language: en
```

Добавить новый перевод:

```bash
# 1. добавить ключ в ErrorCode
# 2. добавить перевод в .po файлы
# 3. скомпилировать
pybabel compile -d app/locales -D messages
```

---

## 📦 Стек

| Компонент | Технология |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 16 |
| Migrations | Alembic |
| Cache | Redis |
| Message Broker | RabbitMQ |
| Task Queue | Celery |
| Validation | Pydantic v2 |
| DI | dependency-injector |
| Localization | Babel (gettext) |
| Primary Key | UUIDv7 |
| Package Manager | uv |

---

## 🔄 Новая миграция

```bash
# 1. создать
uv run alembic revision --autogenerate -m "название"

# 2. применить на primary
uv run alembic upgrade head

# 3. применить на replica
$env:DATABASE_SYNC_URL="postgresql+psycopg://food_tech:food_tech_pass@localhost:5434/food_tech"
uv run alembic upgrade head
$env:DATABASE_SYNC_URL="postgresql+psycopg://food_tech:food_tech_pass@localhost:5433/food_tech"
```

---

## 📡 API

### IAM — Roles

| Метод | Путь | Описание |
|---|---|---|
| `POST` | `/api/v1/roles` | Создать роль |
| `GET` | `/api/v1/roles/{id}` | Получить роль по ID |
| `GET` | `/api/v1/roles` | Список ролей (пагинация) |
| `PUT` | `/api/v1/roles/{id}` | Обновить роль |
| `DELETE` | `/api/v1/roles/{id}` | Удалить роль |

### Пример запроса

```bash
curl -X POST http://localhost:8000/api/v1/roles \
  -H "Content-Type: application/json" \
  -d '{
    "title_ru": "Администратор",
    "value": "admin"
  }'
```

### Пример ответа

```json
{
    "message": "Роль успешно создана",
    "data": {"role_id": "019e4f1c-..."},
    "code": 200,
    "error": null
}
```

---

## 🏛️ Паттерны

### Repository Chain

```
BaseRepo[E]          ← domain, ABC интерфейс
    ↑
RoleRepo[E]          ← domain, специфичный интерфейс
    ↑
BaseRepoImpl[T]      ← shared infra, общий CRUD
    ↑
RoleRepositoryImpl   ← infra, маппинг + специфика
```

### Request Flow

```
HTTP Request
    ↓
Controller (FastAPI)       — валидация схемы (Pydantic)
    ↓
UseCase                    — бизнес оркестрация
    ↓
Domain Entity              — бизнес логика + Value Objects
    ↓
Repository                 — персистентность
    ↓
PostgreSQL
```

### Error Response

```json
{
    "message": "Роль уже существует",
    "data": {"empty": true},
    "code": 409,
    "error": {
        "inner_code": 409,
        "message": "Роль уже существует",
        "detail": null,
        "validation_errors": null,
        "error_trace": null
    }
}
```