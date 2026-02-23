# Mental Math Trainer Server

FastAPI сервер для приложения тренировки устного счёта.

## Запуск

### Разработка (SQLite)

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
uvicorn app.main:app --reload
```

### Продакшн (PostgreSQL в Docker)

```bash
# Запустить PostgreSQL
docker-compose up -d

# Изменить DATABASE_URL в .env на PostgreSQL
DATABASE_URL=postgresql+asyncpg://mm_user:mm_password@localhost:5432/mental_math_db

# Запустить сервер
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Auth
- `POST /api/v1/auth/register` - Регистрация (анонимная или с email)
- `POST /api/v1/auth/login` - Вход по account_key
- `POST /api/v1/auth/login-email` - Вход по email/password
- `GET /api/v1/auth/me` - Информация о текущем пользователе
- `GET /api/v1/auth/me/progress` - Прогресс пользователя

### Tasks
- `GET /api/v1/tasks/levels` - Список уровней сложности
- `GET /api/v1/tasks/topics` - Список тем
- `GET /api/v1/tasks/` - Список задач
- `POST /api/v1/tasks/generate` - Генерация новой задачи
- `POST /api/v1/tasks/validate` - Проверка ответа

### Sessions
- `GET /api/v1/sessions/` - История сессий
- `GET /api/v1/sessions/stats` - Статистика

### Progress
- `GET /api/v1/progress/` - Прогресс пользователя

## Тестирование

```bash
pytest
```
