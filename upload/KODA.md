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
    - *Лежандр, Ландау, Эйлер* (думающие модели, дорогие запросы)
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
│   │       ├── auth.py           # Регистрация/логин/токены (включая анонимную авторизацию по device_id и конвертацию аккаунтов)
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
- `ProblemRead` — чтение задачи (включает объект source: SourceRead и массив tags: TagRead[])
- `ProblemShort` — краткая информация о задаче (включает source: SourceRead)

### app/schemas/tags.py — Схемы для тегов

**Схемы тегов:**
- `TagRead` — чтение тега (id, name, slug)
- `TagMergeRequest` — запрос на объединение тегов (target_tag_id, source_tag_ids)

### app/schemas/users.py — Схемы для пользователей

**Схемы аутентификации:**
- `UserBase` — базовые поля (email, username) (email теперь необязателен)
- `UserCreate` — схема для обычной регистрации (email, username, password)
- `DeviceLogin` — схема для анонимной регистрации/входа по device_id (device_id, secret_key)
- `UserConvert` — схема для конвертации анонимного аккаунта в постоянный (email, password, username)

**Схемы чтения:**
- `UserRead` — чтение пользователя (включает id, email, username, is_anonymous flag, created_at)
- `UserPublicProfile` — публичный профиль (id, email, username, created_at)
- `UserRole` — роль пользователя (admin, moderator, user)

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
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### app/api/v1/auth.py — Регистрация/логин/токены (включая анонимную авторизацию по device_id и конвертацию аккаунтов)

API-эндпоинты для аутентификации пользователей.

**Функции:**
- `POST /register` — обычная регистрация (email, username, password)
- `POST /login` — обычная авторизация (email/username, password)
- `POST /device-register` — анонимная регистрация/авторизация по device_id с созданием/поиском аккаунта, с генерацией весёлых имён
- `POST /convert-account` — конвертация анонимного аккаунта в полноценный (email, password, username)
- `GET /me` — получение профиля текущего пользователя
- Автоматический повторный вход при истечении токена

### app/api/v1/problems.py — Эндпоинты задач

API-эндпоинты для работы с задачами (Problems), включая поддержку источников и тегов.

**Функции:**
- `GET /` — получение списка задач с фильтрацией по источнику, номеру/названию, содержанию условия и тегу
- `POST /` — создание новой задачи с автоматическим созданием источника и тегов
- `GET /{problem_id}` — получение задачи по ID
- `PATCH /{problem_id}` — обновление задачи (источник и теги)
- Сортировка задач по различным критериям

**Фильтрация:**
- `source` — фильтр по названию источника (JOIN с таблицей sources)
- `reference` — фильтр по номеру/названию задачи
- `search` — поиск по тексту условия
- `tag` — фильтр по тегу (JOIN с таблицей tags)

**Схемы:**
- `ProblemCreate` — создание задачи (с source_name и списком тегов)
- `ProblemUpdate` — обновление задачи (с возможностью обновления source_name и тегов)
- `ProblemRead` — чтение задачи (с объектами Source и списка Tag)

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
- `PersonaID` — Enum с доступными персонами: `BASIS` (Кот Базис), `PETROVICH` (Дворник Петрович), `LEGENDRE` (Лежандр), `LANDAU`, `EULER`
- `PERSONA_CONFIGS` — конфигурации для каждой персоны (модель, цена, описание)
- `get_persona_config(persona_id)` — функция получения конфигурации персоны по ID

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
2. **Гл. меню** — выбор действий (решать задачу, анализ концепций, статистика, финансы, профиль)
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
- `device_login()` — анонимная авторизация по device_id
- `login(email, password)` — стандартная авторизация
- `get_me()` — получение профиля текущего пользователя

**Функции для работы с сущностями:**
- `ProblemsApiMixin` — работа с задачами (источники, поиск, создание)
- `SolutionsApiMixin` — работа с решениями (активные решения, создание, завершение)
- `ArtifactsApiMixin` — работа с артефактами (озарения, вопросы, подсказки, загрузка изображений)
- `ConceptsApiMixin` — анализ концепций (AI-анализ задач и решений)
- `BillingApiMixin` — биллинг (баланс, пополнение)
- `GamificationApiMixin` — геймификация (XP, сердца, статистика)
- `CommunityApiMixin` — заглушка для сообщества

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
- `flow_statistics()` — экран статистики и активности, включая количество решенных задач за день
- `flow_finance()` — финансовый модуль
- `flow_concepts()` — анализ концепций
- `flow_profile()` — профиль пользователя
- `flow_admin()` — административные инструменты

### mv_context.py — Системный контекст

Обеспечивает работу с файлами, буфером обмена и выводом.

**Функции:**
- `load_token()`/`save_token()` — работа с токеном авторизации
- `get_or_create_device_creds()` — получение/создание учетных данных устройства
- `capture_clipboard_image()` — захват изображения из буфера обмена
- `delete_file()` — удаление файла
- Вспомогательные функции вывода (`print_header`, `print_success`, `print_error`, `print_info`)
- `input_default()` — ввод с возможностью установки значения по умолчанию

### database.py — Подключение к БД

```python
DATABASE_URL = "postgresql://mv_user:mv_password@localhost:5432/mindvector_db"
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
    device_id = Column(String, unique=True, nullable=True)  # ID устройства для анонимных пользователей
    
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
- `ProblemsApiMixin` — работа с задачами (источники, поиск, создание)
- `SolutionsApiMixin` — работа с решениями (активные решения, создание, завершение)
- `ArtifactsApiMixin` — работа с артефактами (озарения, вопросы, подсказки, загрузка изображений)
- `ConceptsApiMixin` — анализ концепций (AI-анализ задач и решений)
- `BillingApiMixin` — биллинг (баланс, пополнение)
- `GamificationApiMixin` — геймификация (XP, сердца, статистика)
- `CommunityApiMixin` — заглушка для сообщества

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
- `flow_finance()` — финансовый модуль
- `flow_concepts()` — анализ концепций
- `flow_profile()` — профиль пользователя
- `flow_admin()` — административные инструменты

### mv_context.py — Системный контекст

Обеспечивает работу с файлами, буфером обмена и выводом.

**Функции:**
- `load_token()`/`save_token()` — работа с токеном авторизации
- `get_or_create_device_creds()` — получение/создание учетных данных устройства
- `capture_clipboard_image()` — захват изображения из буфера обмена
- `delete_file()` — удаление файла
- Вспомогательные функции вывода (`print_header`, `print_success`, `print_error`, `print_info`)
- `input_default()` — ввод с возможностью установки значения по умолчанию

### database.py — Подключение к БД

```python
DATABASE_URL = "postgresql://mv_user:mv_password@localhost:5432/mindvector_db"
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
    tags = relationship("Tag", secondary="problem_tags", back_populates="problems")
    solutions = relationship("UserSolution", back_populates="problem")

class UserSolution(Base):
    __tablename__ = "user_solutions"
    id, problem_id, user_id, status, personal_difficulty, quality_score, xp_earned
    user_notes, solution_img_path, solution_text, total_minutes
    problem = relationship("Problem", back_populates="solutions")
    sessions = relationship("Session", back_populates="solution")
    epiphanies = relationship("Epiphany", back_populates="solution")
    questions = relationship("Question", back_populates="solution")
    hints = relationship("Hint", back_populates="solution")

class Session(Base):
    __tablename__ = "sessions"
    id, solution_id, start_time, end_time, duration
    solution = relationship("UserSolution", back_populates="sessions")

class Epiphany(Base):
    __tablename__ = "epiphanies"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("user_solutions.id"))
    description = Column(Text, nullable=False)     # Текст/LaTeX описания
    image_path = Column(String, nullable=True)      # Визуализация (опционально)
    magnitude = Column(Integer, default=1)          # 1 — обычное, 2 — сильное, 3 — гениальное
    created_at = Column(DateTime, default=datetime.now)
    solution = relationship("UserSolution", back_populates="epiphanies")

class UserRole(str, enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"

class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    id, email (nullable), hashed_password, username (unique, not null), device_id (unique, nullable), is_anonymous, created_at, updated_at
    role = Column(String, default=UserRole.user, nullable=False, index=True)  # Роли пользователей: admin, moderator, user
    solutions = relationship("UserSolution", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    articles = relationship("Article", back_populates="author")
    gamification = relationship("UserGamification", back_populates="user", uselist=False)
    xp_events = relationship("XpEvent", back_populates="user")

class Comment(Base):
    """Модель комментария"""
    __tablename__ = "comments"
    id, user_id, problem_id, solution_id, article_id, parent_id, body
    created_at, updated_at, is_deleted, is_approved
    user = relationship("User", back_populates="comments")

class Article(Base):
    """Модель статьи/поста"""
    __tablename__ = "articles"
    id, author_id, problem_id, solution_id, article_type, title, slug, summary
    content, is_published, meta, created_at, updated_at
    author = relationship("User", back_populates="articles")

class Vote(Base):
    """Модель голоса/лайка"""
    __tablename__ = "votes"
    id, user_id, target_type, target_id, value, created_at
    user = relationship("User", back_populates="votes")

class Question(Base):
    """Модель вопроса, возникшего в ходе решения задачи"""
    __tablename__ = "questions"
    id, solution_id, body, image_path, answer, created_at, updated_at
    solution = relationship("UserSolution", back_populates="questions")

class Hint(Base):
    """Модель совета от AI по решению задачи"""
    __tablename__ = "hints"
    id, solution_id, hint_text, ai_model, prompt_used, context_image_path
    xp_penalty, status, user_notes, created_at
    solution = relationship("UserSolution", back_populates="hints")

class UserGamification(Base):
    """Модель геймификационного состояния пользователя"""
    __tablename__ = "user_gamification"
    id, user_id, total_xp, current_hearts, max_hearts
    streak_current, streak_best, last_activity_date, created_at, updated_at
    user = relationship("User", back_populates="gamification")

class XpEvent(Base):
    """Модель события изменения XP"""
    __tablename__ = "xp_events"
    id, user_id, solution_id, event_type, delta_xp, meta, created_at
    user = relationship("User", back_populates="xp_events")
    solution = relationship("UserSolution")
```

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
- `GET /balance` — получение текущего баланса пользователя и оставшихся бесплатных запросов
- `POST /top-up` — создание счета на пополнение баланса (интеграция с YooKassa)
- `POST /webhook/yookassa` — обработка уведомлений от платежной системы
- Поддержка разных тарифов AI-персон (бесплатный/платный)
- Интеграция с системой геймификации для учета бесплатных запросов

**Платежная модель:**
- Кот Базис: Бесплатно, с ежедневным лимитом запросов
- Дворник Петрович: 2₽ за запрос
- Лежандр: 10₽ за запрос

### app/api/v1/concepts.py — Эндпоинты анализа концепций

API-эндпоинты для анализа концепций и навыков, необходимых для решения задач и применяемых в решениях.

**Функции:**
- `POST /concepts/analyze/problem/{problem_id}` — запуск AI-анализа задачи для извлечения необходимых знаний (Concept Extraction)
- `POST /concepts/analyze/solution/{solution_id}` — запуск AI-анализа решения для отслеживания примененных навыков (Solution Trace)
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
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Документация API: http://localhost:8000/docs

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

#### test_ocr_real.py

Обновленный интеграционный тест для OCR задач:
- Загрузка изображения задачи
- Запуск OCR с использованием выбранной персоны (по умолчанию Петрович)
- Синхронное ожидание результата
- Проверка качества распознавания

#### test_ocr_solution_real.py

Обновленный интеграционный тест для OCR решений:
- Создание задачи и решения
- Загрузка изображения решения
- Запуск OCR с использованием выбранной персоны (например, Лежандр)
- Синхронное ожидание результата
- Проверка качества распознавания

#### test_client_scenarios.py

Новые интеграционные тесты, проверяющие основные сценарии использования CLI-клиента:

1. **Тест сценария работы с тегами:**
   - Создание задачи с новыми тегами
   - Поиск тегов по названию
   - Слияние тегов (функционал для администратора, role="admin")

2. **Тест сценария генерации ответа на вопрос:**
   - Создание вопроса к решению
   - Загрузка фото контекста (Two-step upload)
   - Генерация AI-ответа через сервис

3. **Тест сценария создания и генерации подсказки (Hint):**
   - Создание черновика подсказки
   - Загрузка фото черновика
   - Генерация AI-подсказки

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

---

## База данных

### Схема PostgreSQL (через Alembic)

```sql
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    slug VARCHAR UNIQUE NOT NULL,
    url_template VARCHAR,
    INDEX ix_sources_name (name),
    INDEX ix_sources_slug (slug)
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    slug VARCHAR UNIQUE NOT NULL,
    INDEX ix_tags_name (name),
    INDEX ix_tags_slug (slug)
);

CREATE TABLE problem_tags (
    problem_id INTEGER REFERENCES problems(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (problem_id, tag_id)
);

CREATE TABLE problems (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id) NOT NULL,
    reference VARCHAR,
    condition_text TEXT,
    condition_img VARCHAR,
    created_at TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR NOT NULL,
    username VARCHAR,
    device_id VARCHAR UNIQUE,
    is_anonymous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE user_solutions (
    id SERIAL PRIMARY KEY,
    problem_id INTEGER REFERENCES problems(id),
    user_id INTEGER REFERENCES users(id),
    status VARCHAR DEFAULT 'active',
    personal_difficulty INTEGER,
    quality_score FLOAT,
    xp_earned FLOAT DEFAULT 0,
    user_notes TEXT,
    solution_img_path VARCHAR,
    solution_text TEXT,
    total_minutes FLOAT DEFAULT 0
);

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    solution_id INTEGER REFERENCES user_solutions(id),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration FLOAT
);

CREATE TABLE epiphanies (
    id SERIAL PRIMARY KEY,
    solution_id INTEGER REFERENCES user_solutions(id),
    description TEXT NOT NULL,
    image_path VARCHAR,
    magnitude INTEGER DEFAULT 1,
    created_at TIMESTAMP
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    solution_id INTEGER REFERENCES user_solutions(id),
    body TEXT NOT NULL,
    image_path VARCHAR,
    answer TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE hints (
    id SERIAL PRIMARY KEY,
    solution_id INTEGER REFERENCES user_solutions(id),
    hint_text TEXT,
    ai_model VARCHAR,
    prompt_used TEXT,
    context_image_path VARCHAR,
    xp_penalty FLOAT DEFAULT 0.0,
    status VARCHAR,
    user_notes TEXT,
    created_at TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    problem_id INTEGER REFERENCES problems(id),
    solution_id INTEGER REFERENCES user_solutions(id),
    article_id INTEGER,
    parent_id INTEGER REFERENCES comments(id),
    body TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES users(id),
    problem_id INTEGER REFERENCES problems(id),
    solution_id INTEGER REFERENCES user_solutions(id),
    article_type VARCHAR,
    title VARCHAR NOT NULL,
    slug VARCHAR UNIQUE NOT NULL,
    summary TEXT,
    content TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_published BOOLEAN DEFAULT FALSE,
    meta JSON
);

CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    target_type VARCHAR NOT NULL,
    target_id INTEGER NOT NULL,
    value INTEGER DEFAULT 1,
    created_at TIMESTAMP
);

CREATE TABLE user_gamification (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    total_xp FLOAT DEFAULT 0.0,
    current_hearts INTEGER DEFAULT 5,
    max_hearts INTEGER DEFAULT 5,
    streak_current INTEGER DEFAULT 0,
    streak_best INTEGER DEFAULT 0,
    last_activity_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE xp_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    solution_id INTEGER REFERENCES user_solutions(id),
    event_type VARCHAR NOT NULL,
    delta_xp FLOAT NOT NULL,
    meta JSON,
    created_at TIMESTAMP
);

-- Финансовые таблицы

CREATE TYPE transaction_type AS ENUM ('deposit', 'spend', 'refund', 'manual');

CREATE TABLE user_balances (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    balance FLOAT DEFAULT 0.0,
    daily_free_uses INTEGER DEFAULT 0,
    last_free_use_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    amount FLOAT NOT NULL,
    transaction_type transaction_type NOT NULL,
    status VARCHAR DEFAULT 'pending',
    description VARCHAR,
    payment_id VARCHAR,  -- ID счета в YooKassa (invoice_id)
    payment_url VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблицы для анализа концепций (Concept Graph)

CREATE TABLE concepts (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    slug VARCHAR UNIQUE NOT NULL,
    description TEXT,
    utility_description TEXT,
    alias_of_id INTEGER REFERENCES concepts(id), -- для дедупликации
    is_public BOOLEAN DEFAULT FALSE,
    author_id INTEGER REFERENCES users(id),
    moderation_status VARCHAR DEFAULT 'pending', -- pending, approved, merged, rejected
    moderation_reason VARCHAR,
    created_at TIMESTAMP
);

CREATE INDEX ix_concepts_name ON concepts (name);
CREATE INDEX ix_concepts_slug ON concepts (slug);
CREATE INDEX ix_concepts_is_public ON concepts (is_public);
CREATE INDEX ix_concepts_alias_of_id ON concepts (alias_of_id);

CREATE TABLE concept_dependencies (
    parent_id INTEGER REFERENCES concepts(id),
    child_id INTEGER REFERENCES concepts(id),
    PRIMARY KEY (parent_id, child_id)
);

CREATE TABLE problem_concepts (
    problem_id INTEGER REFERENCES problems(id),
    concept_id INTEGER REFERENCES concepts(id),
    explanation TEXT,
    relevance FLOAT DEFAULT 1.0,
    PRIMARY KEY (problem_id, concept_id)
);

CREATE TABLE solution_concepts (
    solution_id INTEGER REFERENCES user_solutions(id),
    concept_id INTEGER REFERENCES concepts(id),
    usage_context TEXT,
    PRIMARY KEY (solution_id, concept_id)
);
```

### Миграции Alembic

- **Изменить файл модели models.py**
- **Создать новую миграцию:** `alembic revision --autogenerate -m "описание"`
- **Применить миграции:** `alembic upgrade head`
- **Откатить миграцию:** `alembic downgrade -1`
- **Показать текущую ревизию:** `alembic current`

---

## Docker Compose

**Файл:** `compose.dev.yml`

```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: mindvector_db
    restart: always
    environment:
      POSTGRES_USER: mv_user
      POSTGRES_PASSWORD: mv_password
      POSTGRES_DB: mindvector_db
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

volumes:
  pg_data:
```

---

## TODO и возможности для развития (последние добавленные сверху)

- [ ] Раздел Финансы должен показывать распечатку по расходам баланса из таблицы transactions
- [ ] В mv_run_client Добавить навигатор по задачам/решениям и связанным с ними сущностям - концептам, вопросам, подсказкам, статьям. В нем можно ставить лайки и комменты.
- [ ] Добавить персонажей:
 - Ландау (самые мощные и дорогие модели для самых сложных вопросов уровня Gemini 3 Pro)
 - Понтрягин (агрегирует лучшие модели, работающие только с текстовой модальностью - не видит картинки, но относительно недорогая и очень умная в математике - GLM5, Qwen 3 Max и т.п.). Может быть использован для экономии бюджета после OCR задачи/решения или задач у которых изначально есть текстовый слой.
- [ ] Сделать автоматическую проверку моделей, подгрузку новых и перегруппировку их списков для оптимального выбора
- [ ] Проектирование Flutter клиента. Продумаем интерфейс, дизайн, изображения, видео ролики, звуки. 
- [ ] Создать идеологический модуль(мотиватор), который разъясняет идею приложения и зачем надо решать задачи, дает советы, поддерживает мотивацию.
- [ ] Размещение api сервера на прод - будет доступен на https://kreagenium.ru. Добавить механику деплоя, развертывания новых версий на проде.
- [ ] Отладка механики платежей в продовой версии.  
- [ ] Творческая визуализация задачи. `specs/features/problem_art_visualization.md`
- [ ] Добавить статистику по озарениям, подсказкам и вопросам в mv_run_client.py
- [ ] Реализовать контент-движок для создания статей и генерации видеороликов на основе Manim
- [ ] Добавить ленту активности сообщества
- [ ] Реализовать еженедельный отчёт (weekly digest)
- [ ] **Модерация:** Внедрить асинхронную проверку `is_public` для источников и тегов согласно спецификации `specs/features/moderation.md`.
- [ ] Добавить систему уведомлений о событиях (ошибки, награды)
- [ ] Добавить параметры пейджинга для Problems, UserSolutions

## Было сделано (последние добавлять сверху)

- [x] При выборе задач надо показывать в списке задач также список связанных с ними тегов и концепций
- [x] Баг: Не обновляется Free лимит на новый день
- [x] Открывать ответы от AI подсказок в браузере, как это сделано, для распознавания задач/решений и вопросов 
- [x] Показывать активность задачи в списке задач
- [x] Баг: mv_run_client Нет пути для распознавания концепций из решений
- [x] Баг: При анализе концепций из решения в поле concept->description пишет "Автоматически извлечено из анализа решения", вместо описания концепции
- [x] Баг: mv_run_client ❌ Critical Error: 'MindVectorAPI' object has no attribute 'update_solution_text' - при распознании OCR решения
- [x] Баг: При OCR задачи/решения вставка многострочного текста приводит к ошибкам (вставляется только первая строка)
- [x] Баг: Задачи выводятся не упорядоченными (можно упорядочить по id)
- [x] **Image Processing API Refactor:** Рефакторинг API-клиента и добавление вызова распознавателя задач и решений из фото с поддержкой разных AI-персон (Petrovich, Legendre и др.) через синхронную обработку OCR вместо фоновой
- [x] **AI Service Integration:** Перенос OCR-функций из `app/services/image_processing.py` в `app/services/ai_service.py` с интеграцией разных AI-персон для обработки изображений задач и решений
- [x] **Sync OCR Processing:** Замена асинхронной фоновой обработки изображений на синхронную с возвратом результата клиенту для эндпоинтов `/api/v1/content/process-image/problem/{problem_id}` и `/api/v1/content/process-image/solution/{solution_id}`
- [x] **Interactive OCR Workflow:** Добавление интерактивного вызова OCR в сессиях решения задач и в меню управления задачами/решениями в `mv_screens.py`
- [x] **Persona-Based OCR:** Поддержка разных AI-персон (basis, petrovich, legendre) для обработки изображений через параметр `persona` в API-запросах
- [x] **Add OCR functionality to mv_run_client:** Добавить в mv_run_client.py запуск преобразования изображений задачи и решения в md текст с поддержкой разных AI-персон
- [x] **FastAPI Refactor:** Обновить эндпоинты загрузки изображений (Uploads) для Questions и Epiphanies.
- [x] **Refactoring клиентского приложения:** Удален старый `mindvector.py`, добавлены новые модули `mv_run_client.py`, `mv_api.py`, `mv_screens.py`, `mv_context.py`, реализующие более структурированное консольное приложение
- [x] **Gamification API Updates:** Удалены комментарии, указывающие на необходимость авторизации некоторых эндпоинтов, обновлён эндпоинт `get_daily_activity` для воспроизведения логики из `mv_stats.py`
- [x] **Concept Graph & AI Analysis:** Добавлена система анализа концепций - автоматическое извлечение требуемых и примененных знаний из задач и решений (AI Concept Extraction & Solution Trace)
- [x] **Concept Endpoints:** Добавлены эндпоинты `/api/v1/concepts` для анализа концепций с поддержкой разных AI-персон
- [x] **Concept Models:** Добавлены модели `Concept`, `ProblemConcept`, `SolutionConcept`, `ConceptDependency` для хранения знаний и их связей
- [x] **Concept Schemas:** Добавлены схемы в `app/schemas/concepts.py` для работы с концепциями
- [x] **Knowledge Graph:** Реализована база для построения графа зависимостей между понятиями (Concept Dependency Graph)
- [x] **Auth Bug Fix:** Исправлена ошибка авторизации, добавлено поле device_id к пользователям с приоритетным использованием device_id для аутентификации устройств, обновлена логика поиска пользователей по device_id, добавлена генерация весёлых имён для анонимных пользователей.
- [x] **Billing System:** Реализована платежная система с поддержкой YooKassa, балансом пользователей и разными тарифами AI-персон
- [x] **AI Personas:** Реализована поддержка разных AI-персон (Кот Базис, Дворник Петрович, Лежандр) с разными ценами и возможностями
- [x] **Financial Module:** Добавлен модуль `mv_finance.py` для управления биллингом и выбора персон
- [x] **Billing Endpoints:** Добавлены эндпоинты `/api/v1/billing` для работы с балансом и оплатой
- [x] **Payment Service:** Добавлена интеграция с YooKassa через модуль `app/services/payment_service.py`
- [x] **Financial Models:** Добавлены модели `UserBalance` и `Transaction` для хранения информации о балансе и транзакциях
