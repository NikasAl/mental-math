# KODA.md — Инструкции для работы с проектом

## Обзор проекта

**Название:** MindVector — система отслеживания прогресса в решении задач. А также мотиватор и учитель/репетитор, помогающий находить ошибки и разбираться в непонятном.
Будущий Android-Клиент будет называться "Лежандр"

**Тип проекта:** Консольное Python-приложение + REST API на FastAPI с PostgreSQL-базой данных
В будущем на основе mv_run_client.py будет написан Android-Клиент на Flutter

**Назначение:** Приложение предназначено для учёта времени, затраченного на решение математических и других задач, с элементами геймификации (система XP). Позволяет:
- Вести библиотеку задач с условиями (текст или фото)
- Отслеживать время работы над каждой задачей творческими сессиями
- Сохранять оценку пользователя личной сложности и качества решения
- Просматривать статистику активности и заработанных очков
- Получать AI-подсказки по решению задач от LLM моделей через OpenRouter или в custom режиме
- Использовать REST API для интеграции с Android-клиентом (в дальнейшем будет частью приложения)
- Общаться с сообществом (комментарии, статьи, голосования)
- **Автоматическая модерация контента:** Гибридная система видимости (Private по умолчанию -> Public после проверки AI)
- **Визуализация общения с AI:** Использование виртуальных персонажей для разного уровня задач:
    - *Кот Базис* (легкая модель, бесплатная с лимитом)
    - *Дворник Петрович* (интуитивная flash-модель, может ошибаться, платная)
    - *Лежандр* (ученый, строгий стиль, средняя стоимость)
    - *Лев Ландау* (премиум модели для сложнейших задач: Gemini 3 Pro, Claude Sonnet)
    - *Лев Понтрягин* (текстовые модели для математических задач, без vision, экономичный)
- **Поддержка разных AI-персон для OCR:** Возможность использовать различные ИИ-модели для - распознавания текста с изображений задач и решений (с разными уровнями точности и стоимости)
- Преобразовывать изображения условий и решений задач в markdown текст с формулами (OCR) с поддержкой разных AI-персон
- Встроенные платежи и биллинг система (YooKassa)
- Классифицировать задачи по источникам и тегам
- **Онтология знаний:** Строить граф зависимостей между понятиями, необходимыми для решения задач (Knowledge Graph)
- **Анализ концепций:** AI-анализ задач и решений для автоматического извлечения требуемых и примененных знаний/навыков (Concept Extraction & Trace)
- **AI Концепт-Анализ:** Автоматическое выявление необходимых знаний в задачах и примененных методов в решениях с помощью ИИ-персон (Кот Базис, Лежандр и др.)
- Фиксировать вопросы, возникшие в процессе решения и отвечать на них через AI либо самим пользователем
- **Инструмент мышления:** Трекинг не только учебных, но и бытовых/инженерных задач на техпроцессы и формальную логику (например: "диагностика двигателя" -> рассуждения -> решение)
- **Система ролей пользователей:** Поддержка различных ролей (admin, moderator, user) с соответствующими правами доступа
- **Стабильность и надежность:** Защита от дублирования активных решений, автоматическое обновление токенов при истечении, retry-логика для надежности соединения
- **Отображение статистики:** Показывает количество решенных задач за день
- **Улучшенная обработка изображений:** Интеграция OCR-распознавания задач и решений из фото

---

## Технологический стек

| Компонент | Технология |
|-----------|------------|
| Язык программирования | Python 3 |
| Веб-фреймворк | FastAPI (async) |
| База данных | PostgreSQL 15 |
| ORM | SQLAlchemy 2.x |
| Миграции БД | Alembic |
| Контейнеризация | Docker + Docker Compose |
| Работа с изображениями | Pillow (PIL) + ImageGrab (для буфера обмена) |
| HTTP-запросы | httpx (асинхронные запросы на сервере), requests (синхронные запросы с поддержкой retry на CLI клиенте mv_run_client)
| Тестирование | pytest, pytest-asyncio, httpx |
| Конфигурация | python-dotenv + pydantic-settings |
| Аутентификация | JWT (python-jose, passlib) |
| ASGI-сервер | uvicorn |
| Платежная система | YooKassa |
| AI-персоны | Enum (определение доступных ИИ-моделей и их характеристик) |

---

## Структура проекта

```
<root>
├── app/                          # FastAPI приложение
│   ├── main.py                   # Точка входа FastAPI
│   ├── core/                     # Ядро приложения
│   │   ├── config.py             # Настройки проекта (env, JWT, БД, OpenRouter)
│   │   ├── personas.py           # Определение AI-персон (Кот Базис, Петрович, Лежандр и др.)
│   │   └── security.py           # JWT-логика, зависимости для auth
│   ├── db/                       # Работа с базой данных
│   │   ├── session.py            # Создание engine/session, async-обёртка
│   │   └── base.py               # Подключение моделей и метаданных
│   ├── schemas/                  # Pydantic-схемы
│   │   ├── problems.py
│   │   ├── solutions.py
│   │   ├── tags.py
│   │   ├── sessions.py
│   │   ├── epiphanies.py
│   │   ├── users.py
│   │   ├── comments.py
│   │   ├── articles.py
│   │   ├── votes.py
│   │   ├── questions.py
│   │   ├── hints.py
│   │   ├── concepts.py           # Схемы для анализа концепций (Concept, ProblemConcept, SolutionConcept)
│   │   ├── gamification.py       # Схемы геймификации (UserGamification, XpEvent)
│   │   └── __init__.py
│   ├── api/                      # REST API эндпоинты
│   │   └── v1/
│   │       ├── router.py         # Главный роутер v1
│   │       ├── auth.py           # Регистрация/логин/токены (account_key авторизация, конвертация аккаунтов)
│   │       ├── problems.py       # Эндпоинты задач (с поддержкой источников и тегов)
│   │       ├── solutions.py      # Эндпоинты решений
│   │       ├── sessions.py       # Эндпоинты сессий
│   │       ├── epiphanies.py     # Эндпоинты озарений
│   │       ├── users.py          # Эндпоинты пользователей (вкл. конвертацию анонимных аккаунтов)
│   │       ├── comments.py       # Эндпоинты комментариев
│   │       ├── articles.py       # Эндпоинты статей
│   │       ├── votes.py          # Эндпоинты голосов
│   │       ├── questions.py      # Эндпоинты вопросов
│   │       ├── hints.py          # Эндпоинты подсказок
│   │       ├── sources.py        # Эндпоинты источников
│   │       ├── tags.py           # Эндпоинты тегов
│   │       ├── gamification.py   # Эндпоинты геймификации (XP, hearts, streak)
│   │       ├── image_processing.py # Эндпоинты обработки изображений (OCR)
│   │       ├── uploads.py        # Единый эндпоинт загрузки изображений для всех сущностей
│   │       ├── images.py         # Отдача прикреплённых фото сущностей (GET, для просмотра в браузере)
│   │       ├── billing.py        # Эндпоинты биллинга и оплаты
│   │       ├── concepts.py       # Эндпоинты анализа концепций и навыков (Concept Graph)
│   │       └── __init__.py
│   ├── utils/                    # Утилиты проекта
│   │   └── name_generator.py     # Генератор забавных имен для анонимных пользователей
│   └── services/                 # Бизнес-логика
│       ├── xp.py                 # Расчёт XP и бонусов
│       ├── gamification.py       # Геймификация (hearts, streak, XP events)
│       ├── llm_client.py         # Клиент OpenRouter API (асинхронные httpx-запросы)
│       ├── ai_service.py         # AI-сервисы (генерация подсказок, ответов на вопросы, анализ концепций, OCR с поддержкой персон)
│       ├── content_engine.py     # Контент-движок (генерация статей)
│       ├── payment_service.py    # Сервис оплаты (YooKassa SDK)
│       └── image_processing.py   # OCR преобразование изображений в текст (включая итеративный пайплайн)
├── mv_run_client.py              # Основное консольное приложение (ранее mindvector_client.py)
├── mv_api.py                     # API клиентский слой
├── mv_screens.py                 # UI экраны и интерактивные сессии
├── mv_context.py                 # Системный контекст (токены, буфер обмена, вывод)
├── image_manager.py              # Централизованное управление изображениями
├── app.conf                      # Конфигурация (API ключи)
├── .env                          # Переменные окружения
├── .gitignore                    # Исключения для Git
├── .token                        # Файл с токеном авторизации от клиента API
├── requirements.txt              # Зависимости проекта
├── tests/                        # Тестовая инфраструктура
│   ├── conftest.py               # pytest-фикстуры (БД, HTTP-клиент, моки)
│   ├── benchmarks/               # Тесты производительности
│   │   ├── test_ocr_real.py             # Тесты OCR на реальных изображениях задач
│   │   ├── test_ocr_solution_real.py    # Тесты OCR на реальных изображениях решений
│   │   ├── test_ocr_benchmark.py        # Тесты производительности разных моделей OCR
│   │   └── test_ocr_iterative.py        # Тесты итеративного OCR пайплайна
│   └── integration/
│       ├── test_android_flows.py        # Интеграционные тесты REST API
│       ├── test_client_scenarios.py     # Тесты основных сценариев из клиента
│       ├── test_auth_flows.py           # Тесты аутентификации (device auth, account conversion)
│       └── test_stability_flows.py      # Тесты стабильности (токены, защита от дублей решений)
├── database.py                   # Подключение к PostgreSQL (SQLAlchemy engine + sessionmaker)
├── models.py                     # SQLAlchemy модели (Problem, UserSolution, Session, Epiphany, User, Comment, Article, Vote, Question, Hint, UserGamification, XpEvent)
├── compose.dev.yml               # Docker Compose конфигурация для PostgreSQL
├── alembic.ini                   # Конфигурация Alembic
├── pytest.ini                    # Конфигурация pytest (с игнорированием DeprecationWarning от passlib)
├── scripts/                      # Скрипты для обслуживания
│   ├── db_dump_restore.sh        # Скрипт бэкапа/восстановления БД с автоматическим бэкапом изображений
│   └── img_backup_restore.sh     # Скрипт бэкапа/восстановления изображений
├── specs/                        # Спецификации для генерации кода проекта
│   ├── done/
│   │   ├── features/
│   │   │   └── cli_interactive_session.md  # Спецификация CLI-интерактивной сессии
│   │   └── maintenance/
│   │       ├── db_dump_restore.md
│   │       └── img_path_refg.md
│   └── features/
│       ├── moderaton.md             # Спецификация системы модерации контента
│       ├── problem_art_visualization.md  # Спецификация Creative Visualization (Art Mode)
│       └── concept_graph.md         # Спецификация Графа Знаний и Анализа Навыков
└── alembic/                      # Миграции Alembic
    ├── env.py
    ├── README
    ├── script.py.mako
    └── versions/
        ├── 1bdd3e2b1db5_initial_tables.py  # Начальная миграция
        ├── 6ca9c3f4f146_add_epiphanies_table.py  # Таблица озарений
        ├── a1b2c3d4e5f6_add_community_tables_users_comments_articles_votes.py  # Таблицы сообщества
        ├── b2c3d4e5f6a7_add_questions_hints_article_types.py  # Вопросы, подсказки, типы статей
        ├── c3d4e5f6a7b8_add_gamification_tables_user_gamification_xp_events.py  # UserGamification, XpEvent
        ├── d4e5f6a7b8c9_add_solution_text_field.py  # Поле solution_text для OCR
        ├── d5e5f6a7b8c9_source_tags.py  # Рефакторинг источников и тегов (новые таблицы sources, tags, problem_tags)
        ├── 01086dafc8c3_hint_ai_nullable.py  # Добавление nullable полей в таблицу hints (status, user_notes)
        ├── 7b023b3a8f0f_users_auth_changes.py  # Изменения аутентификации (email nullable, username unique not null, is_anonymous flag)
        ├── 558b09021d3e_add_device_id_to_users.py  # Добавление device_id к пользователям (уникальный индекс)
        ├── 58eaf3cd8828_add_financial_tables.py  # Таблицы для биллинга (transactions, user_balances)
        ├── ca89043ba7a0_add_concepts.py  # Таблицы для анализа концепций (concepts, problem_concepts, solution_concepts, concept_dependencies)
        ├── abb3021379a3_add_role_to_users.py  # Добавление ролей к пользователям (admin, moderator, user)
        └── 7ea78ae6b39f34fdc1c86759d69703a8ea457934 # Исправление бага дублирования активных решений
# Папки для изображений (создаются автоматически)
├── images/               # Централизованное хранилище
│   ├── conditions/       # Условия задач
│   ├── solutions/        # Решения и вспомогательные изображения (озарения, вопросы, подсказки)
│   └── temp/             # Временные файлы при обработке
├── to_delete/            # Устаревшие файлы (после миграции)
└── __pycache__/

---

## Схемы данных (Pydantic)

### app/schemas/problems.py — Схемы для задач

**Схемы источников (Sources):**
- `SourceRead` — чтение источника (id, name, slug, url_template)

**Схемы задач:**
- `ProblemBase` — базовые поля (reference, condition_text)
- `ProblemCreate` — создание задачи (source_name, tags как список строк)
- `ProblemUpdate` — обновление задачи (source_name, tags как список строк)
- `ProblemRead` — чтение задачи (включает source: SourceRead, added_by: UserPublicProfile и массив tags: TagRead[])
- `ProblemShort` — краткая информация о задаче (включает source: SourceRead)
- `ProblemListResponse` — ответ со списком задач и пейджингом (items, total, limit, offset)

### app/schemas/tags.py — Схемы для тегов

**Схемы тегов:**
- `TagRead` — чтение тега (id, name, slug)
- `TagMergeRequest` — запрос на объединение тегов (target_tag_id, source_tag_ids)

### app/schemas/users.py — Схемы для пользователей

**Схемы аутентификации:**
- `UserBase` — базовые поля (email, username) (email теперь необязателен)
- `UserCreate` — схема для обычной регистрации (email, username, password)
- `AccountLoginRequest` — схема для входа по account_key (account_key)
- `UserConvert` — схема для конвертации анонимного аккаунта в постоянный (email, password, username)

**Схемы чтения:**
- `UserRead` — чтение пользователя (включает id, email, username, is_anonymous flag, created_at)
- `UserPublicProfile` — публичный профиль (id, email, username, created_at)
- `UserRole` — роль пользователя (admin, moderator, user)

### app/schemas/solutions.py — Схемы для решений

**Схемы решений:**
- `SolutionBase` — базовые поля (problem_id, status, personal_difficulty, quality_score, user_notes)
- `SolutionCreate` — создание решения
- `SolutionUpdate` — обновление решения
- `SolutionRead` — чтение решения (включает added_by: UserPublicProfile)
- `SolutionListResponse` — ответ со списком решений и пейджингом (items, total, limit, offset)

### app/schemas/concepts.py — Схемы для концепций

**Схемы концепций:**
- `ConceptBase` — базовые поля концепции (name, description, utility_description)
- `ConceptCreate` — создание концепции (name, description, utility_description)
- `ConceptRead` — чтение концепции (включает id, slug, description, utility_description, создание и связи)
- `ConceptUpdate` — обновление концепции (description, utility_description, moderation_status)

**Схемы связей концепций:**
- `ProblemConceptRead` — связь задачи и концепции (problem_id, concept_id, relevance, explanation)
- `SolutionConceptRead` — связь решения и концепции (solution_id, concept_id, usage_context)
- `ConceptDependencyCreate` — создание зависимости между концепциями (parent_id, child_id)

---

## Модули приложения

### app/main.py — FastAPI приложение

FastAPI-приложение с REST API для интеграции с Android-клиентом.

**Функции:**
- Точка входа FastAPI-сервера
- CORS middleware для Android-клиента
- Подключение всех API-роутеров
- Эндпоинты `/` и `/health` для проверки состояния

**Запуск:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### app/api/v1/auth.py — Регистрация/логин/токены (account_key авторизация)

API-эндпоинты для аутентификации пользователей.

**Архитектура account_key:**
Единый ключ `account_key` для авторизации на всех устройствах. Формат: `acc_` + 24 байта в base64 (~32 символа, ~192 бита энтропии).

**Эндпоинты:**
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/account-login` | Вход/регистрация по account_key |
| POST | `/register` | Классическая регистрация (email, username, password) |
| POST | `/login` | Вход по email/pass, возвращает account_key |
| GET | `/me` | Профиль текущего пользователя |

**Логика account-login:**
1. Если account_key найден → вход в существующий аккаунт
2. Если не найден → создание нового анонимного аккаунта
3. При входе по email/pass сервер возвращает account_key для сохранения на клиенте

**Конвертация аккаунта:** `PATCH /users/me/convert` — привязка email/password к анонимному аккаунту.

**Модель User:**
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=True)      # nullable для анонимов
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    account_key = Column(String, unique=True, nullable=True)  # единый ключ для всех устройств
    is_anonymous = Column(Boolean, default=False)
    role = Column(String, default="user")  # admin, moderator, user
```

### app/api/v1/problems.py — Эндпоинты задач

API-эндпоинты для работы с задачами (Problems), включая поддержку источников и тегов.

**Функции:**
- `GET /` — получение списка задач с фильтрацией и пейджингом
- `POST /` — создание новой задачи с автоматическим созданием источника и тегов, проставление user_id
- `GET /{problem_id}` — получение задачи по ID
- `PATCH /{problem_id}` — обновление задачи (источник и теги)
- Сортировка по убыванию ID (новые задачи сверху)

**Фильтрация:**
- `source` — фильтр по названию источника (JOIN с таблицей sources)
- `reference` — фильтр по номеру/названию задачи
- `search` — поиск по тексту условия
- `tag` — фильтр по тегу (JOIN с таблицей tags)
- `user_id` — фильтр по пользователю, добавившему задачу

**Пейджинг:**
- `limit` — количество записей (по умолчанию 20, макс 100)
- `offset` — смещение для пейджинга

**Схемы:**
- `ProblemCreate` — создание задачи (с source_name и списком тегов)
- `ProblemUpdate` — обновление задачи (с возможностью обновления source_name и тегов)
- `ProblemRead` — чтение задачи (с объектами Source, added_by и списка Tag)
- `ProblemListResponse` — ответ с пейджингом (items, total, limit, offset)

### app/api/v1/tags.py — Эндпоинты тегов

API-эндпоинты для работы с тегами задач.

**Функции:**
- `GET ` — поиск тегов по названию (частичное совпадение), возвращает список объектов TagRead (изменилось: убран слэш в пути)
- `POST /merge` — объединение нескольких тегов в один (только для администратора с ролью admin), перемещает все связи задач с исходных тегов к целевому тегу

**Схемы:**
- `TagRead` — чтение тега (id, name, slug)
- `TagMergeRequest` — запрос на объединение тегов (target_tag_id, source_tag_ids)

### app/api/v1/gamification.py — Эндпоинты геймификации

API-эндпоинты для работы с системой геймификации.

**Функции:**
- `GET /daily-stats` — получение статистики за день, включая количество решенных задач
- `GET /xp-events` — получение событий получения XP
- `GET /leaderboard` — получение таблицы лидеров

### app/core/config.py — Конфигурация

Настройки проекта через pydantic-settings v2 и environment variables.

**Параметры:**
- `DATABASE_URL` — PostgreSQL connection string
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` — JWT настройки
- `OPENROUTER_API_KEY` — ключ для AI-подсказок
- `API_V1_PREFIX` — префикс API (`/api/v1`)
- `DEBUG` — режим отладки

### app/core/personas.py — Определение AI-персон

Определение доступных AI-персон для различных задач (OCR, подсказки, анализ концепций).

**Классы и константы:**
- `PersonaID` — Enum с доступными персонами: `BASIS` (Кот Базис), `PETROVICH` (Дворник Петрович), `LEGENDRE` (Лежандр), `LANDAU` (Лев Ландау), `PONTRYAGIN` (Лев Понтрягин)
- `PersonaConfig` — конфигурация персоны с параметрами:
  - `name` — отображаемое имя
  - `cost` — стоимость в рублях за запрос
  - `models` — список моделей (fallback chain)
  - `system_prompt_add` — дополнение к системному промпту
  - `error_phrases` — фразы при ошибках
  - `is_free_tier` — бесплатный тариф
  - `supports_vision` — поддержка изображений (False для Понтрягина)
- `PERSONAS` — словарь конфигураций для каждой персоны

**Особенности персон:**
- **Кот Базис** (0₽) — бесплатный с дневным лимитом, мультимодальный
- **Дворник Петрович** (2₽) — дешевый, простые объяснения, мультимодальный
- **Лежандр** (10₽) — научный стиль с LaTeX, мультимодальный
- **Лев Ландау** (25₽) — премиум модели для сложных задач, мультимодальный
- **Лев Понтрягин** (5₽) — текстовые модели, без vision, экономный вариант для задач с текстовым слоем

### app/core/security.py — JWT-безопасность

Функции и зависимости для аутентификации:

- `verify_password(plain, hashed)` — проверка пароля
- `get_password_hash(password)` — хеширование пароля
- `create_access_token(data, expires_delta)` — создание JWT
- `decode_access_token(token)` — декодирование JWT
- `get_current_user_id()` — FastAPI зависимость для получения user_id из токена
- Поддержка ролей пользователей (admin, moderator, user)

### app/db/session.py — Async-обёртка над SQLAlchemy

Асинхронная зависимость `get_db()` для FastAPI:

- Использует `fastapi.concurrency.run_in_threadpool` для sync-операций БД
- Предоставляет `SessionLocal` из `database.py`
- Гранулярный контроль сессий в обработчиках

### app/services/xp.py — Расчёт XP

Чистые функции для расчёта очков опыта:

- `calc_base_xp(total_minutes, difficulty, quality)` — базовый XP: `время × сложность × качество`
- `calc_epiphanies_bonus(epiphanies, difficulty)` — бонус за озарения: `сила × сложность × 50`
- `calc_total_xp(...)` — общий XP с учётом всех бонусов

### app/services/ai_service.py — AI-сервисы

Сервисы для работы с ИИ-моделями.

**Функции:**
- `generate_hint()` — генерация подсказки к задаче
- `answer_question()` — ответ на вопрос пользователя
- `analyze_concepts_in_problem()` — анализ концепций в задаче
- `analyze_concepts_in_solution()` — анализ концепций в решении
- `ocr_from_image()` — OCR-распознавание текста с изображения с использованием различных AI-персон

### mv_run_client.py — Основной интерактивный клиент

Функция `main()` запускает интерактивный процесс через `ScreenManager`:

1. **Авторизация** — через `ensure_auth()` с поддержкой device_id
2. **Гл. меню** — выбор действий (решать задачу, анализ концепций, статистика, библиотека, финансы, профиль)
3. **Решение задачи** — через `flow_solve_shortcut()` с поддержкой продолжения активных решений
4. **Интерактивная сессия** — команды: `h` (hint), `e` (epiphany), `q` (question), `s` (status), `f` (finish)
5. **Анализ концепций** — через `flow_concepts()` с выбором AI-персоны
6. **Статистика** — через `flow_statistics()` с отображением данных по дням и количества решенных задач за день
7. **Финансы** — через `flow_finance()` с управлением балансом
8. **Профиль** — через `flow_profile()` с возможностью привязки email
9. **Администрирование** — через `flow_admin()` (только для администраторов)

**Интерактивные команды в сессии (mv_screens.py):**
- **`h` (Hint)** — добавление подсказки с учетом контекста решения
- **`e` (Epiphany)** — добавление озарения "на лету" в процессе сессии
- **`q` (Question)** — работа с вопросами (добавление, список, ответы)
- **`s` (Status)** — просмотр текущей длительности сессии и статистики
- **`v` (View)** — просмотр и редактирование текущего решения, включая OCR текста
- **`f` (Finish)** — завершение сессии и переход к финализации решения

**Функция `flow_solution_session(solution_id, existing_minutes)`:**
- Интерактивная сессия решения задачи
- Отображение приглашения `mv-session > `
- Запись сессии в БД при завершении
- Возможность финализации решения с оценками сложности и качества

### mv_api.py — API клиентский слой

Реализует взаимодействие с REST API сервера.

**Базовые функции:**
- `BaseApiMixin` — общая логика запросов, с обработкой истечения токена и повторными попытками
- `account_login()` — вход/регистрация по account_key (единый ключ для всех устройств)
- `login(email, password)` — стандартная авторизация, сохраняет полученный account_key
- `get_me()` — получение профиля текущего пользователя

**Функции для работы с сущностями:**
- `ProblemsApiMixin` — работа с задачами (источники, поиск, создание)
- `SolutionsApiMixin` — работа с решениями (активные решения, создание, завершение)
- `ArtifactsApiMixin` — работа с артефактами (озарения, вопросы, подсказки, загрузка изображений, `get_epiphanies`)
- `ConceptsApiMixin` — анализ концепций (AI-анализ задач и решений), `get_concepts_by_solution(solution_id)`
- `BillingApiMixin` — биллинг (баланс, пополнение)
- `GamificationApiMixin` — геймификация (XP, сердца, статистика)
- `CommentsApiMixin` — комментарии: `get_comments_by_problem`, `get_comments_by_solution`, `get_comments_by_article`, `create_comment`, `delete_comment`
- `VotesApiMixin` — голоса: `create_or_update_vote(target_type, target_id, value)`, `get_vote_summary(target_type, target_id)`
- `CommunityApiMixin` — статьи: `get_articles(limit, offset, problem_id, solution_id)`, `get_article(id_or_slug)`
- Просмотр фото сущностей: `get_entity_image_url(category, entity_id)` (URL по токену), `get_entity_image_bytes(category, entity_id)` (скачивание с токеном для вставки в страницу просмотра)

### mv_screens.py — UI экраны и интерактивные сессии

Реализует пользовательские экраны и интерактивные сессии.

**Функции:**
- `ScreenManager` — основной класс управления экранами
- `_draw_bar()` — визуализация данных в виде ASCII-бара
- `_select_persona_interactive()` — выбор AI-персоны
- `_select_tags_interactive()` — интерактивный выбор тегов
- `ensure_auth()` — проверка авторизации
- `flow_main_menu()` — главное меню приложения
- `flow_solve_shortcut()` — сокращенный путь к решению задачи
- `_flow_select_task()` — выбор задачи из библиотеки
- `flow_solution_session()` — интерактивная сессия решения
- `flow_statistics()` — экран статистики и активности
- `flow_library()` — раздел «Библиотека»: навигатор по задачам, решениям и связанным сущностям (концепты, вопросы, подсказки, озарения, статьи); комментарии и лайки; просмотр фото через страницу в браузере
- `flow_finance()` — финансовый модуль
- `flow_concepts()` — анализ концепций
- `flow_profile()` — профиль пользователя
- `flow_admin()` — административные инструменты
- Навигатор: `_manage_problem_content` (детали задачи, фото условия, комментарии, лайки), `_manage_solution_detail` (детали решения, фото, вопросы/подсказки/озарения/статьи, комментарии, лайки), `_manage_article_detail`, `_show_comments_flow`, `_show_votes_flow`

### mv_context.py — Системный контекст

Обеспечивает работу с файлами, буфером обмена и выводом.

**Функции:**
- `load_token()`/`save_token()` — работа с токеном авторизации
- `get_or_create_account_key()` — получение/создание учетных данных устройства
- `capture_clipboard_image()` — захват изображения из буфера обмена
- `delete_file()` — удаление файла
- `open_editor_browser(text)` — открытие редактора Markdown/LaTeX в браузере (шаблон `HTML_EDITOR_TEMPLATE`)
- `open_entity_viewer_browser(title, text=None, image_bytes=None, image_media_type)` — страница просмотра сущности: заголовок, текст (Markdown + MathJax), кнопка «Показать фото»; изображение подставляется как base64 (загружается клиентом по токену), чтобы браузер не делал запросов без авторизации
- Вспомогательные функции вывода (`print_header`, `print_success`, `print_error`, `print_info`)
- `input_default()` — ввод с возможностью установки значения по умолчанию

### database.py — Подключение к БД

```python
DATABASE_URL = "postgresql://mm_user:mm_password@localhost:5430/mentalmath_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Генератор сессий для использования в with"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
```

### app/db/session.py — Async-обёртка над SQLAlchemy

Асинхронная зависимость `get_db()` для FastAPI:

```python
async def get_db() -> Generator[Session, None, None]:
    """
    Async-зависимость для FastAPI, отдающая SQLAlchemy Session.
    Внутри обработчиков БД-запросы выполняются через run_in_threadpool.
    """
```

### models.py — SQLAlchemy модели

```python
class VoteTargetType(enum.Enum):
    """Типы сущностей, за которые можно голосовать"""
    problem = "problem"
    solution = "solution"
    article = "article"
    comment = "comment"


class ArticleType(enum.Enum):
    """Типы статей"""
    problem_explainer = "problem_explainer"
    motivational = "motivational"
    weekly_digest = "weekly_digest"
    epiphanies_collection = "epiphanies_collection"


class XpEventType(enum.Enum):
    """Типы событий XP"""
    session = "session"
    solution_completed = "solution_completed"
    epiphany_bonus = "epiphany_bonus"
    hint_penalty = "hint_penalty"
    manual_adjust = "manual_adjust"


class UserRole(str, enum.Enum):
    """Роли пользователей"""
    admin = "admin"
    moderator = "moderator"
    user = "user"


class Source(Base):
    """Справочник источников задач"""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    url_template = Column(String, nullable=True)

    problems = relationship("Problem", back_populates="source_obj")

class Tag(Base):
    """Теги для категоризации задач"""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    problems = relationship("Problem", secondary="problem_tags", back_populates="tags")

# Таблица ассоциации Many-to-Many для тегов
class ProblemTag(Base):
    __tablename__ = "problem_tags"

    problem_id = Column(Integer, ForeignKey("problems.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class Problem(Base):
    __tablename__ = "problems"
    id, source_id, reference, condition_text, condition_img, created_at
    # Связь с решениями
    source_obj = relationship("Source", back_populates="problems")
    tags = relationship("Tag", secondary="problem_tags", back_populates="tags")
    solutions = relationship("UserSolution", back_populates="problem")

class UserSolution(Base):
    __tablename__ = "user_solutions"
    id, problem_id, user_id, status, personal_difficulty, quality_score, xp_earned
    user_notes, solution_img_path, solution_text, total_minutes
    # Связь с задачей
    problem = relationship("Problem", back_populates="solutions")
    user = relationship("User", back_populates="solutions")
    sessions = relationship("Session", back_populates="solution")

class User(Base):
    __tablename__ = "users"
    id, email, username, hashed_password, created_at, is_active, is_verified
    role = Column(Enum(UserRole), default=UserRole.user)  # Новое поле для роли пользователя
    is_anonymous = Column(Boolean, default=False)  # Флаг анонимного пользователя
    account_key = Column(String, unique=True, nullable=True)  # Ключ аккаунта
        
    solutions = relationship("UserSolution", back_populates="user")
    gamification = relationship("UserGamification", uselist=False, back_populates="user")

class Session(Base):
    __tablename__ = "sessions"
    id, solution_id, start_time, end_time, duration_minutes, notes
    solution = relationship("UserSolution", back_populates="sessions")

class Epiphany(Base):
    __tablename__ = "epiphanies"
    id, solution_id, content, strength, created_at
    solution = relationship("UserSolution", back_populates="epiphanies")

class Question(Base):
    __tablename__ = "questions"
    id, solution_id, content, answer, is_answered, created_at
    solution = relationship("UserSolution", back_populates="questions")

class Hint(Base):
    __tablename__ = "hints"
    id, solution_id, content, ai_generated, created_at, status, user_notes
    solution = relationship("UserSolution", back_populates="hints")

class Comment(Base):
    __tablename__ = "comments"
    id, target_type, target_id, user_id, content, created_at
    user = relationship("User", back_populates="comments")

class Article(Base):
    __tablename__ = "articles"
    id, title, content, author_id, article_type, created_at
    author = relationship("User", back_populates="authored_articles")

class Vote(Base):
    __tablename__ = "votes"
    id, user_id, target_type, target_id, vote_type, created_at
    user = relationship("User", back_populates="votes")

class UserGamification(Base):
    __tablename__ = "user_gamification"
    id, user_id, hearts, streak_count, current_level, xp_total
    user = relationship("User", back_populates="gamification")

class XpEvent(Base):
    __tablename__ = "xp_events"
    id, user_id, event_type, xp_amount, description, created_at
    user = relationship("User", back_populates="xp_events")

class Transaction(Base):
    __tablename__ = "transactions"
    id, user_id, amount, transaction_type, status, created_at
    user = relationship("User", back_populates="transactions")

class UserBalance(Base):
    __tablename__ = "user_balances"
    id, user_id, balance, currency, updated_at
    user = relationship("User", back_populates="balance")

class Concept(Base):
    __tablename__ = "concepts"
    id, name, slug, description, utility_description, created_at, updated_at, moderation_status
    # Связи с задачами и решениями через промежуточные таблицы

class ProblemConcept(Base):
    __tablename__ = "problem_concepts"
    id, problem_id, concept_id, relevance, explanation, created_at
    problem = relationship("Problem", back_populates="problem_concepts")
    concept = relationship("Concept", back_populates="problem_concepts")

class SolutionConcept(Base):
    __tablename__ = "solution_concepts"
    id, solution_id, concept_id, usage_context, created_at
    solution = relationship("UserSolution", back_populates="solution_concepts")
    concept = relationship("Concept", back_populates="solution_concepts")

class ConceptDependency(Base):
    __tablename__ = "concept_dependencies"
    id, parent_id, child_id, relationship_type, created_at
    parent = relationship("Concept", foreign_keys=[parent_id], back_populates="child_dependencies")
    child = relationship("Concept", foreign_keys=[child_id], back_populates="parent_dependencies")

# Добавление обратных связей для Concept
Concept.problem_concepts = relationship("ProblemConcept", back_populates="concept")
Concept.solution_concepts = relationship("SolutionConcept", back_populates="concept")
Concept.child_dependencies = relationship("ConceptDependency", foreign_keys="[ConceptDependency.parent_id]", back_populates="parent")
Concept.parent_dependencies = relationship("ConceptDependency", foreign_keys="[ConceptDependency.child_id]", back_populates="child")
```
- `login(email, password)` — стандартная авторизация
- `get_me()` — получение профиля текущего пользователя

**Функции для работы с сущностями:**
- `ProblemsApiMixin`, `SolutionsApiMixin`, `ArtifactsApiMixin` (включая `get_epiphanies`), `ConceptsApiMixin` (включая `get_concepts_by_solution`), `BillingApiMixin`, `GamificationApiMixin`
- `CommentsApiMixin` — комментарии по задаче/решению/статье, создание, удаление
- `VotesApiMixin` — лайки/дизлайки, сводка голосов
- `CommunityApiMixin` — статьи с фильтрами, `get_article(id_or_slug)`
- `get_entity_image_url()`, `get_entity_image_bytes()` — для просмотра фото сущностей в браузере

### mv_screens.py — UI экраны и интерактивные сессии

Реализует пользовательские экраны и интерактивные сессии. Раздел «Библиотека» (`flow_library`) — навигатор по задачам, решениям, концептам, вопросам, подсказкам, озарениям, статьям с комментариями и лайками; просмотр фото через страницу в браузере.

**Конфигурация (app.conf):**
- `OPENROUTER_API_KEY` — ключ API OpenRouter
- `HINT_MODE` — режим работы (`custom` или `api`)
- `HINT_MODEL` — модель для API (по умолчанию `google/gemini-3-flash-preview`)

### image_manager.py — Централизованное управление изображениями

Модуль для унификации работы с изображениями во всех модулях приложения.

**Константы:**
- `IMAGES_ROOT` — корневая папка `images`
- `DIRS` — словарь подпапок: `condition` → `conditions`, `solution` → `solutions`

**Функции:**
- `_ensure_dir(category, date_str)` — создаёт структуру `images/<category>/<YYYYMMDD>`
- `sanitize_filename(text)` — очищает имя файла от недопустимых символов
- `get_full_path(category, db_path)` — преобразует путь из БД в полный путь ФС
- `save_upload_file(file, category, filename_prefix)` — асинхронное сохранение UploadFile в FastAPI
- `save_clipboard_image(category, naming_parts)` — сохраняет изображение из буфера в WebP
**Важно:** Для сущностей, связанных с решением (Epiphany, Question, Hint), теперь используется категория `solution`. Тип сущности передается как суффикс в `naming_parts` (например, `[sol_id, "question"]` → `..._question_...webp`).

**Формат путей в БД:** `<YYYYMMDD>/<имя>_<HHMMSS>.webp` (без префикса категории)

### app/api/v1/billing.py — Эндпоинты биллинга и оплаты

API-эндпоинты для работы с биллингом и платежами пользователей.

**Функции:**
- `GET /balance` — получение текущего баланса, автоматически проверяет и обновляет pending счета через YooKassa API
- `GET /transactions` — получение истории транзакций с пейджингом
- `POST /top-up` — создание счета на пополнение баланса (интеграция с YooKassa Invoice API)
- `POST /check-pending` — принудительная проверка всех pending счетов пользователя
- `GET /invoice/{invoice_id}/status` — проверка статуса конкретного счета
- `POST /webhook/yookassa` — обработка уведомлений от платежной системы (опционально)
- Поддержка разных тарифов AI-персон (бесплатный/платный)
- Интеграция с системой геймификации для учета бесплатных запросов

**Архитектура оплаты (Polling вместо Webhooks):**
Поскольку webhook от YooKassa не гарантируется, используется polling-модель:
1. При создании счета (`/top-up`) создается транзакция со статусом `pending` и сохраняется `invoice_id`
2. При запросе баланса (`/balance`) автоматически проверяются все pending счета через YooKassa API
3. Если счет оплачен (`succeeded`) — обновляется статус транзакции и начисляется баланс
4. Если счет отменен (`canceled`) — обновляется статус транзакции

**Эндпоинты:**
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/balance` | Баланс + автообновление pending счетов |
| GET | `/transactions` | История транзакций (пейджинг) |
| POST | `/top-up?amount=N` | Создать счет на оплату |
| POST | `/check-pending` | Принудительная проверка счетов |
| GET | `/invoice/{id}/status` | Статус конкретного счета |
| POST | `/webhook/yookassa` | Webhook (опционально) |

**Платежная модель:**
- Кот Базис: Бесплатно, с ежедневным лимитом запросов
- Дворник Петрович: 2₽ за запрос
- Лежандр: 10₽ за запрос
- Лев Ландау: 25₽ за запрос
- Лев Понтрягин: 5₽ за запрос

**Модели данных:**
- `Transaction` — транзакция (user_id, amount, status, payment_id, payment_url)
- `UserBalance` — баланс пользователя (balance, daily_free_uses)

### app/services/payment_service.py — Сервис оплаты

Функции для работы с YooKassa Invoice API:

**Функции:**
- `create_invoice(amount, description, user_id)` — создание счета, возвращает (invoice_id, payment_url)
- `get_invoice_info(invoice_id)` — получение статуса через SDK
- `check_invoice_status_direct(invoice_id)` — прямой HTTP запрос к YooKassa API для получения полной информации о счете

**YooKassa API для проверки счета:**
```bash
curl https://api.yookassa.ru/v3/invoices/{invoice_id} \
  -X GET \
  -u <shop_id>:<secret_key> \
  -H 'Content-Type: application/json'
```

**Ответ содержит:**
- `status` — pending/succeeded/canceled
- `payment_details` — информация о платеже
- `cart` — корзина с суммой
- `metadata` — пользовательские данные (user_id)

### app/api/v1/concepts.py — Эндпоинты анализа концепций

API-эндпоинты для анализа концепций и навыков, необходимых для решения задач и применяемых в решениях.

**Функции:**
- `POST /concepts/analyze/problem/{problem_id}` — запуск AI-анализа задачи для извлечения необходимых знаний (Concept Extraction)
- `POST /concepts/analyze/solution/{solution_id}` — запуск AI-анализа решения для отслеживания примененных навыков (Solution Trace)
- `GET /concepts/by-solution/{solution_id}` — получение списка связей решение–концепт (SolutionConceptRead) для навигатора
- `POST /concepts/deduplicate` — запуск процесса дедупликации концепций (только для администраторов)
- Поддержка разных AI-персон для анализа (определяет качество и стоимость анализа)
- Интеграция с биллинговой системой для списания средств за платный анализ

**Сценарии использования:**
- Анализ задачи: выявление требуемых математических понятий и их важности
- Анализ решения: отслеживание примененных методов и навыков
- Построение графа зависимостей между понятиями (Knowledge Graph)

### app/api/v1/uploads.py — Единый эндпоинт загрузки изображений

Реализует паттерн **Two-Step Upload** для загрузки изображений к различным сущностям.

**Функции:**
- `POST /{category}/{entity_id}` — загрузка изображения для существующей сущности
- Категории: `condition` (Problem), `solution` (UserSolution), `epiphany`, `question`, `hint`
- Проверка прав доступа (владелец сущности) перед загрузкой файла
- Использование `image_manager.save_upload_file()` для сохранения файла
- Обновление соответствующего поля в БД (например, `condition_img`, `solution_img_path`, `context_image_path`)

**Принцип работы:**
1. Сначала создается сущность (задача, решение, озарение и т.д.) через соответствующий эндпоинт (JSON)
2. Затем загружается изображение через единый эндпоинт `/uploads/{category}/{entity_id}` (multipart/form-data)
3. При загрузке выполняется проверка авторизации и обновление поля изображения в БД

### app/api/v1/images.py — Отдача прикреплённых фото сущностей

Эндпоинт для просмотра изображений сущностей в браузере (клиент запрашивает с токеном и подставляет изображение в локальную страницу).

**Функции:**
- `GET /images/{category}/{entity_id}` — возвращает файл изображения (`FileResponse`)
- Категории: `condition`, `solution`, `epiphany`, `question`, `hint` (как в uploads)
- Проверка прав: для `condition` — любой авторизованный пользователь; для остальных — владелец решения
- Используется клиентом через `get_entity_image_bytes()` (запрос с токеном), результат вставляется в HTML-страницу просмотра как base64, чтобы браузер не делал отдельного запроса без авторизации

Комментарии (`app/api/v1/comments.py`): `GET /comments/by-problem/{problem_id}`, `GET /comments/by-solution/{solution_id}`, `GET /comments/by-article/{article_id}` (пагинация limit/offset), `POST /comments` (создание), `DELETE /comments/{comment_id}`. Голоса (`app/api/v1/votes.py`): `POST /votes` (создание/обновление), `GET /votes/summary?target_type=&target_id=`.

### app/api/v1/image_processing.py — Эндпоинты обработки изображений (OCR)

Эндпоинты для обработки изображений и преобразования в текст с поддержкой разных AI-персон.

**Функции:**
- `POST /problem/{problem_id}?persona={persona_id}` — синхронная обработка изображения условия задачи с возвратом результата (по умолчанию используется petrovich)
- `POST /solution/{solution_id}?persona={persona_id}` — синхронная обработка изображения решения с возвратом результата (по умолчанию используется petrovich)
- Поддержка разных AI-персон через параметр `persona` (basis, petrovich, legendre и др.)
- Возвращает распознанный текст условия или решения
- Требует авторизации

### app/services/image_processing.py — OCR преобразование изображений в текст

Модуль для преобразования изображений задач и решений в текстовый формат с LaTeX формулами через LLM.

**Функции:**
- `process_problem_image(problem_id, condition_img_path, model)` — обработка изображения условия задачи
- `process_solution_image(solution_id, solution_img_path, model)` — обработка изображения решения
- `process_solution_image_iterative(solution_img_path, vision_model, logic_model)` — итеративный OCR пайплайн с критикой и уточнением
- Использует OpenRouter API для вызова моделей с визуальным восприятием

**Итеративный OCR (conversational/reverse role):**
- Состоит из 3 этапов: Draft (черновик от визуальной модели), Critique (критика от логической модели), Refinement (уточнение визуальной моделью)
- Повышает точность распознавания за счет обнаружения и исправления ошибок

### app/services/ai_service.py — AI-сервисы (подсказки, ответы на вопросы, OCR)

Модуль для генерации AI-подсказок, ответов на вопросы пользователей и OCR-обработки изображений.

**Функции:**
- `generate_answer_for_question(question, solution, problem)` — генерация ответа на вопрос пользователя с использованием контекста задачи и решения
- `analyze_problem_concepts(problem, db, user_id, persona_id)` — AI-анализ задачи для извлечения требуемых знаний (Concept Extraction)
- `analyze_solution_concepts(solution, problem, db, user_id, persona_id)` — AI-анализ решения для выявления примененных навыков (Solution Trace)
- `process_problem_image_with_persona(problem_id, image_path, db, user_id, persona_id)` — OCR-обработка изображения условия задачи с использованием выбранной AI-персоны
- `process_solution_image_with_persona(solution_id, image_path, db, user_id, persona_id)` — OCR-обработка изображения решения с использованием выбранной AI-персоны
- Интеграция с изображениями: условие задачи и изображение вопроса (если имеется)
- Использует системный промпт репетитора и вызывает LLM через OpenRouter API
- Поддержка разных AI-персон (Кот Базис, Дворник Петрович, Лежандр)
- Проверка баланса пользователя и ограничение по платежам

### app/services/payment_service.py — Сервис оплаты

Модуль для интеграции с платежной системой YooKassa.

**Функции:**
- `create_invoice(amount, description, user_id)` — создание счета на оплату
- `get_invoice_info(invoice_id)` — получение информации о состоянии счета
- Интеграция с бизнес-логикой приложения для обработки платежей
- Обработка вебхуков от платежной системы

### app/api/v1/sources.py — Эндпоинты источников

API-эндпоинты для работы с источниками задач.

**Функции:**
- `GET /` — получение списка источников с возможностью поиска по названию
- Поддерживает фильтрацию через параметр `search`
- Возвращает список объектов `SourceRead` с сортировкой по имени

### app/api/v1/questions.py — Эндпоинты вопросов (обновлено)

API-эндпоинты для работы с вопросами, возникающими в процессе решения задач.

**Функции:**
- Все предыдущие эндпоинты (CRUD операции для вопросов)
- `POST /{question_id}/generate` — генерация AI-ответа на вопрос пользователя с использованием контекста задачи и решения
- Возвращает обновленный объект вопроса с добавленным полем `answer`


### mv_finance.py — Финансовый модуль

Консольный интерфейс управления биллингом и AI-персонами.

**Функции:**
- `finance_menu(api)` — основное меню финансового раздела
- `print_balance_card(balance_data)` — отображение информации о балансе и оставшихся запросах
- `top_up_flow(api)` — интерактивное пополнение баланса через YooKassa
- `select_persona_interactive()` — выбор AI-персоны для генерации (Кот Базис, Петрович, Лежандр)
- Интеграция с REST API для работы с платежами
- Поддержка ежедневного лимита бесплатных запросов для Кота Базиса

### app/services/content_engine.py — Движок контента и мотивации

Модуль для генерации мотивирующих текстов и пояснений по решению задач.

**Функции:**
- `generate_motivational_quote()` — генерация случайной мотивационной цитаты из предопределенного списка (еще не реализовано)
- `explain_why_solve_problems()` — объяснение значения решения задач для развития мышления
- Интеграция с CLI для отображения мотивационных материалов пользователю (не реализовано)

---

## Запуск приложения

### 1. Запуск PostgreSQL в Docker

```bash
docker compose -f compose.dev.yml up -d
```

### 2. Применение миграций

```bash
alembic upgrade head
```

### 3. Запуск модулей приложения

**FastAPI сервер (REST API):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```
Документация API: http://localhost:8001/mm/docs

Эндпоинт для тестирования: https://kreagenium.ru/mm/api/v1

**Основное консольное приложение (клиент):**
```bash
python mv_run_client.py
```


### Остановка PostgreSQL

```bash
docker compose -f compose.dev.yml down
```

---

## Тестовая инфраструктура

Проект использует `pytest` и `pytest-asyncio` для написания интеграционных тестов REST API.

### Структура тестов

```
tests/
├── conftest.py                   # pytest-фикстуры
│   ├── setup_test_database       # Создание/удаление БД 'mindvector_test_db'
│   ├── db_session                # Транзакционная сессия с откатом (isolation)
│   ├── async_client              # AsyncClient FastAPI с подменённой БД
│   ├── temp_image_storage        # Подмена пути к хранилищу картинок
│   └── mock_llm_service          # Мок для OpenRouter API
└── integration/
    ├── test_android_flows.py     # Сценарии (E2E) для Android-клиента
    ├── test_client_scenarios.py  # Тесты основных сценариев из CLI-клиента
    └── test_finance_and_personas.py  # Тесты биллинга и AI-персон
```

#### test_finance_and_personas.py

Новые интеграционные тесты, проверяющие функциональность биллинга и AI-персон:

1. **Тест биллинга:**
   - Проверка начального баланса пользователя
   - Создание счета на пополнение
   - Эмуляция вебхука оплаты
   - Проверка обновленного баланса после оплаты

2. **Тест бесплатной персоны (Кот Базис):**
   - Запрос к бесплатной персоне
   - Проверка уменьшения лимита бесплатных запросов
   - Проверка, что баланс не меняется

3. **Тест платной персоны при недостатке средств:**
   - Запрос к платной персоне (Дворник Петрович) с нулевым балансом
   - Проверка ошибки 402 Payment Required

4. **Тест платной персоны при достатке средств:**
   - Пополнение баланса
   - Запрос к платной персоне
   - Проверка списания средств с баланса

Тесты используют фикстуры и моки для изоляции и проверки функциональности без обращения к внешним сервисам.


Тесты используют фикстуры и моки для изоляции и проверки функциональности без обращения к внешним сервисам.

### Фикстуры

| Фикстура | Назначение |
|----------|------------|
| `event_loop` | Event loop для pytest-asyncio (session scope) |
| `setup_test_database` | Создаёт чистую `mindvector_test_db` и таблицы перед сессией |
| `db_session` | Сессия с авто-ROLLBACK после каждого теста |
| `async_client` | HTTP-клиент с переопределённой зависимостью `get_db` |
| `mock_llm_service` | Мокает `requests.post` для LLM-вызовов (возвращает "Test AI Hint Response") |
| `temp_image_storage` | Временное хранилище изображений для тестов загрузки |

### Сценарии (test_android_flows.py)

1. **Сценарий 1: Холодный старт** — регистрация, логин, получение профиля, проверка `UserGamification`
2. **Сценарий 2: Путь решателя** — создание задачи, старт решения, сессия, озарение, завершение, расчёт XP
3. **Сценарий 3: Система подсказок** — запрос подсказки (мок), штраф XP, финализация
4. **Сценарий 4: Сообщество** — комментирование, голосование, проверка статистики

### Запуск тестов

Для запуска требуется установленный `pytest` и запущенный Docker-контейнер с PostgreSQL.

1.  **Запуск всех тестов:**

    ```bash
    pytest tests/ -v
    ```

2.  **Запуск конкретного файла:**

    ```bash
    pytest tests/integration/test_android_flows.py -v
    ```

*Примечание: Файл `pytest.ini` в корне проекта автоматически добавляет текущую директорию в `PYTHONPATH`, что решает проблемы с импортом модуля `app`.*

### Зависимости для тестов

Дополнительные пакеты (установить в виртуальное окружение):

```bash
pip install pytest pytest-asyncio httpx sqlalchemy psycopg2-binary pillow
```

---

## Установка зависимостей

```bash
pip install -r requirements.txt
# для тестов
pip install -r requirements-tests.txt
```

**Содержимое requirements.txt:**
```
Pillow
python-dotenv
requests
sqlalchemy
alembic
psycopg2-binary
# FastAPI и зависимости
fastapi
uvicorn[standard]
pydantic
pydantic-settings
python-jose[cryptography]
# Фиксация версии bcrypt обязательна для работы passlib
passlib[bcrypt]
bcrypt==4.0.1
email-validator
yookassa
```

---

## Архитектурные решения

1. **ORM SQLAlchemy 2.x** — декларативный подход с автоматическим управлением сессиями
2. **PostgreSQL 15** — надёжная реляционная БД в Docker-контейнере
3. **Alembic миграции** — версионирование схемы БД, возможность отката
4. **Геймификация XP** — формула: `время (мин) × сложность (1-5) × качество (0.1-1.0)`
5. **Озарения (Epiphanies)** — бонус XP за ключевые идеи: `сила × сложность × 50`
6. **Централизованное хранение изображений** — модуль `image_manager.py` управляет путями и сохранением
7. **Конвертация в WebP** — все изображения сохраняются в формате WebP для экономии места
8. **Структура путей** — в БД хранится относительный путь `<YYYYMMDD>/<имя>_<HHMMSS>.webp`
9. **FastAPI + JWT** — REST API с аутентификацией для Android-клиента

---

## Соглашения по коду

| Аспект | Соглашение |
|--------|------------|
| Именование функций | snake_case |
| Именование констант | UPPER_SNAKE_CASE |
| Отступы | 4 пробела |
| Подключение к БД | `DATABASE_URL` в `database.py`, сессия через `SessionLocal` |
| Пути к папкам | pathlib.Path с `mkdir(parents=True, exist_ok=True)` |
| Комментарии | Для сложной логики и описание назначения функций |
| FastAPI/Pydantic | Схемы в `app/schemas/`, эндпоинты в `app/api/v1/`, зависимости через `Depends` |
