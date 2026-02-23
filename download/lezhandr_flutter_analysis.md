# Анализ CLI клиента MindVector и план миграции на Flutter

## 1. Общая архитектура текущего решения

### 1.1 Структура модулей

```
mv_run_client.py          → Точка входа (main())
mv_api.py                 → API клиент (REST API)
mv_screens.py             → UI экраны и flows
mv_context.py             → Контекст (токены, буфер обмена, вывод)
```

### 1.2 Паттерн проектирования

Клиент использует **Mixins** для разделения функциональности API:

```python
class MindVectorAPI(BaseApiMixin, ProblemsApiMixin, SolutionsApiMixin, 
                    ArtifactsApiMixin, ConceptsApiMixin, BillingApiMixin, 
                    GamificationApiMixin, CommunityApiMixin, ContentApiMixin):
    pass
```

---

## 2. Детальный анализ API функций

### 2.1 BaseApiMixin — Базовая логика

| Функция | Метод | Описание | Flutter аналог |
|---------|-------|----------|----------------|
| `_request()` | internal | Базовый HTTP запрос с retry при 401 | Dio + Interceptors |
| `device_login()` | POST /auth/device-register | Анонимная авторизация по device_id | SecureStorage + DeviceInfo |
| `login()` | POST /auth/login | Авторизация email/password | Form + Dio |
| `get_me()` | GET /users/me | Профиль пользователя | User provider |
| `link_email()` | PATCH /users/me/convert | Конвертация анонимного аккаунта | Form диалог |

**Ключевые особенности:**
- Автоматическое обновление токена при 401
- Сохранение токена в файл `.token`
- Генерация device_id и secret_key для анонимной авторизации

### 2.2 ProblemsApiMixin — Работа с задачами

| Функция | Endpoint | Описание |
|---------|----------|----------|
| `get_sources()` | GET /sources | Список источников задач |
| `get_problems()` | GET /problems?search=&source= | Поиск задач |
| `get_problem(id)` | GET /problems/{id} | Получить задачу |
| `create_problem()` | POST /problems | Создать задачу |
| `update_problem_text()` | PATCH /problems/{id} | Обновить текст условия |
| `get_tags()` | GET /tags?search= | Поиск тегов |
| `merge_tags()` | POST /tags/merge | Объединение тегов (admin) |

### 2.3 SolutionsApiMixin — Работа с решениями

| Функция | Endpoint | Описание |
|---------|----------|----------|
| `get_active_solutions()` | GET /solutions?status=active | Активные решения |
| `get_solution(id)` | GET /solutions/{id} | Получить решение |
| `get_solutions(problem_id)` | GET /solutions?problem_id= | Решения задачи |
| `create_solution()` | POST /solutions | Начать решение |
| `finish_solution()` | PATCH /solutions/{id} | Завершить с оценками |
| `update_solution_text()` | PATCH /solutions/{id} | Обновить текст решения |
| `post_session()` | POST /sessions | Записать сессию работы |

### 2.4 ArtifactsApiMixin — Артефакты решения

| Функция | Endpoint | Описание |
|---------|----------|----------|
| `upload_image()` | POST /uploads/{category}/{id} | Загрузка изображения |
| `create_epiphany()` | POST /epiphanies | Создать озарение |
| `get_questions()` | GET /questions/by-solution/{id} | Вопросы решения |
| `get_question(id)` | GET /questions/{id} | Получить вопрос |
| `create_question()` | POST /questions | Создать вопрос |
| `answer_question()` | PATCH /questions/{id} | Ответить на вопрос |
| `generate_question_answer()` | POST /questions/{id}/generate | AI-ответ на вопрос |
| `create_hint_draft()` | POST /hints/draft | Черновик подсказки |
| `generate_hint()` | POST /hints/{id}/generate | AI-генерация подсказки |
| `get_hints()` | GET /hints/by-solution/{id} | Подсказки решения |
| `update_hint()` | PATCH /hints/{id} | Обновить подсказку |

### 2.5 ContentApiMixin — OCR и контент

| Функция | Endpoint | Описание |
|---------|----------|----------|
| `trigger_problem_ocr()` | POST /content/process-image/problem/{id} | OCR условия |
| `trigger_solution_ocr()` | POST /content/process-image/solution/{id} | OCR решения |

**Параметры:** `?persona=basis|petrovich|legendre`

### 2.6 ConceptsApiMixin — Анализ концепций

| Функция | Endpoint | Описание |
|---------|----------|----------|
| `analyze_problem()` | POST /concepts/analyze/problem/{id} | Карта знаний задачи |
| `analyze_solution()` | POST /concepts/analyze/solution/{id} | Трейс навыков решения |
| `deduplicate_concepts()` | POST /concepts/deduplicate | Дедупликация (admin) |

### 2.7 BillingApiMixin — Финансы

| Функция | Endpoint | Описание |
|---------|----------|----------|
| `get_billing_balance()` | GET /billing/balance | Баланс и лимиты |
| `create_topup()` | POST /billing/top-up | Пополнение через YooKassa |

### 2.8 GamificationApiMixin — Геймификация

| Функция | Endpoint | Описание |
|---------|----------|----------|
| `get_gamification_me()` | GET /gamification/me | XP, сердца, стрик |
| `get_daily_activity()` | GET /gamification/activity/daily | Активность по дням |

### 2.9 CommunityApiMixin — Сообщество

| Функция | Endpoint | Описание |
|---------|----------|----------|
| `get_articles()` | GET /articles | Статьи (заглушка) |

---

## 3. UI Flows — Экраны и сценарии

### 3.1 Главное меню (flow_main_menu)

```
┌─────────────────────────────────────┐
│         ГЛАВНОЕ МЕНЮ                │
├─────────────────────────────────────┤
│ 1. 🚀 Решать задачу (Сессия)        │
│ 2. 🧠 Анализ концепций              │
│ 3. 📊 Статистика                    │
│ 4. 📂 Библиотека и Контент          │
│ 7. 💰 Финансы                       │
│ 8. 👤 Профиль                       │
│ 9. 🛠 Админка (только admin)        │
│ 0. Выход                            │
└─────────────────────────────────────┘
```

### 3.2 Решение задачи (flow_solve_shortcut)

```
1. Проверка активных решений
   ├─ Если есть → показать список для продолжения
   └─ Иначе → переход к выбору новой задачи

2. Выбор задачи (_flow_select_task_for_solving)
   ├─ Выбор источника из списка
   ├─ Поиск/выбор задачи
   └─ Или создание новой задачи

3. Интерактивная сессия (flow_solution_session)
   ├─ Команды: h, e, q, s, v, f
   └─ Запись времени сессии

4. Финализация решения
   ├─ Оценка сложности (1-5)
   ├─ Оценка качества (0.1-1.0)
   ├─ Заметки
   └─ Фото решения (опционально)
```

### 3.3 Интерактивная сессия (flow_solution_session)

**Команды:**

| Команда | Действие | Описание |
|---------|----------|----------|
| `h` | Hint | Создать запрос подсказки |
| `e` | Epiphany | Записать озарение |
| `q` | Question | Работа с вопросами |
| `s` | Status | Показать время сессии |
| `v` | View | Просмотр/редактирование решения |
| `f` | Finish | Завершить сессию |

### 3.4 Библиотека (flow_library)

```
┌─────────────────────────────────────┐
│     📂 БИБЛИОТЕКА И КОНТЕНТ         │
├─────────────────────────────────────┤
│ Выбор источника                     │
│   ↓                                 │
│ Список задач источника              │
│   ├─ [ID] 📝/🖼️ Reference 🟢        │
│   └─ Теги и концепции               │
│                                     │
│ Действия над задачей:               │
│   1. 👁 Просмотр/OCR Условия        │
│   2. 📂 Посмотреть решения          │
└─────────────────────────────────────┘
```

### 3.5 Статистика (flow_statistics)

```
┌─────────────────────────────────────┐
│      📊 СТАТИСТИКА И ПРОГРЕСС       │
├─────────────────────────────────────┤
│ ⭐ XP: 1234.5                       │
│ ❤️ Сердца: 5/5                      │
│ 🔥 Стрик: 7 дн.                     │
│ ✅ Решено сегодня: 3                │
│                                     │
│ 📊 АКТИВНОСТЬ (7 дней)              │
│ ┌──────────────────────────────────┐│
│ │ Дата    | Время | XP | График    ││
│ │ Сегодня | 45    | 120 |█████ (3) ││
│ │ ...     | ...   | ... |...       ││
│ └──────────────────────────────────┘│
└─────────────────────────────────────┘
```

### 3.6 Анализ концепций (flow_concepts)

```
┌─────────────────────────────────────┐
│       🧠 АНАЛИЗ КОНЦЕПЦИЙ           │
├─────────────────────────────────────┤
│ 1. Анализ задачи (Карта Знаний)     │
│    → Выбор задачи                   │
│    → Выбор персоны                  │
│    → Результат: концепции + relevance│
│                                     │
│ 2. Анализ решения (Трейс Навыков)   │
│    → Выбор источника                │
│    → Выбор задачи                   │
│    → Выбор решения                  │
│    → Результат: концепции + context │
└─────────────────────────────────────┘
```

### 3.7 Финансы (flow_finance)

```
┌─────────────────────────────────────┐
│          💳 БАЛАНС: 50.00 ₽         │
├─────────────────────────────────────┤
│ 🐱 Кот Базис (Free): 3/5 запросов   │
│                                     │
│ 1. ➕ Пополнить баланс              │
│ 2. 🔄 Обновить                      │
│ 0. 🔙 Назад                         │
└─────────────────────────────────────┘
```

### 3.8 Профиль (flow_profile)

```
┌─────────────────────────────────────┐
│          👤 ИМЯ_ПОЛЬЗОВАТЕЛЯ        │
├─────────────────────────────────────┤
│ ID: 123                             │
│ Статус: Анонимный / Зарегистрирован │
│                                     │
│ Для анонимных:                      │
│   → Привязать Email                 │
│   → Пароль                          │
│   → Username                        │
└─────────────────────────────────────┘
```

---

## 4. AI Персоны

| Персона | Модель | Цена | Описание |
|---------|--------|------|----------|
| 🐱 Кот Базис | basis | Бесплатно | Может лениться, лимит запросов |
| 🧹 Петрович | petrovich | 2 ₽ | Gemini Flash, быстро |
| 🧐 Лежандр | legendre | 10 ₽ | Gemini Pro, точно |
| 📐 Ландау | landau | — | Дорогая думающая модель |
| 🔢 Эйлер | euler | — | Дорогая думающая модель |

---

## 5. Ключевые особенности для мобильного клиента

### 5.1 Работа с изображениями (камера)

**Текущее решение (CLI):**
- Захват из буфера обмена через `PIL.ImageGrab`
- Загрузка через `POST /uploads/{category}/{id}`

**Flutter решение:**
- `image_picker` для камеры и галереи
- `camera` для прямого доступа к камере
- Предпросмотр перед отправкой
- Сжатие изображений

### 5.2 OCR распознавание

**Категории изображений:**
- `condition` — условие задачи
- `solution` — решение
- `epiphany` — схема озарения
- `question` — контекст вопроса
- `hint` — контекст подсказки

### 5.3 Хранение токенов

**Текущее:** файлы `.token` и `.device_creds`

**Flutter:** `flutter_secure_storage`

### 5.4 Редактор Markdown

**Текущее:** HTML шаблон с marked.js + MathJax в браузере

**Flutter:** `flutter_markdown` + `math_keyboard` для формул

---

## 6. План миграции на Flutter

### 6.1 Архитектура Flutter приложения

```
lib/
├── main.dart
├── app.dart
├── core/
│   ├── config/
│   │   └── app_config.dart           # Конфигурация API_URL и т.д.
│   ├── theme/
│   │   ├── app_theme.dart            # Тема приложения
│   │   └── colors.dart               # Цветовая палитра
│   ├── router/
│   │   └── app_router.dart           # GoRouter навигация
│   └── constants/
│       └── personas.dart             # AI персоны
│
├── data/
│   ├── models/                       # DTO модели
│   │   ├── user.dart
│   │   ├── problem.dart
│   │   ├── solution.dart
│   │   ├── session.dart
│   │   ├── epiphany.dart
│   │   ├── question.dart
│   │   ├── hint.dart
│   │   ├── concept.dart
│   │   ├── source.dart
│   │   ├── tag.dart
│   │   ├── gamification.dart
│   │   └── billing.dart
│   │
│   ├── repositories/                 # Репозитории (data layer)
│   │   ├── auth_repository.dart
│   │   ├── problems_repository.dart
│   │   ├── solutions_repository.dart
│   │   ├── artifacts_repository.dart
│   │   ├── concepts_repository.dart
│   │   ├── billing_repository.dart
│   │   └── gamification_repository.dart
│   │
│   ├── services/                     # API сервисы
│   │   ├── api_client.dart           # Dio + Interceptors
│   │   ├── auth_service.dart
│   │   └── upload_service.dart
│   │
│   └── storage/
│       ├── token_storage.dart        # SecureStorage
│       └── device_storage.dart       # Device credentials
│
├── domain/
│   ├── entities/                     # Business entities
│   └── usecases/                     # Use cases (опционально)
│
├── presentation/
│   ├── providers/                    # Riverpod providers
│   │   ├── auth_provider.dart
│   │   ├── problems_provider.dart
│   │   ├── solutions_provider.dart
│   │   ├── session_provider.dart     # Активная сессия
│   │   ├── gamification_provider.dart
│   │   └── theme_provider.dart
│   │
│   ├── screens/                      # Экраны
│   │   ├── splash/
│   │   │   └── splash_screen.dart
│   │   ├── auth/
│   │   │   └── login_screen.dart
│   │   ├── main_menu/
│   │   │   └── main_menu_screen.dart
│   │   ├── problems/
│   │   │   ├── problem_list_screen.dart
│   │   │   ├── problem_detail_screen.dart
│   │   │   └── problem_create_screen.dart
│   │   ├── solutions/
│   │   │   ├── solution_session_screen.dart
│   │   │   ├── solution_finalize_screen.dart
│   │   │   └── active_solutions_screen.dart
│   │   ├── library/
│   │   │   └── library_screen.dart
│   │   ├── statistics/
│   │   │   └── statistics_screen.dart
│   │   ├── concepts/
│   │   │   ├── concept_analysis_screen.dart
│   │   │   └── concept_result_screen.dart
│   │   ├── billing/
│   │   │   └── billing_screen.dart
│   │   ├── profile/
│   │   │   └── profile_screen.dart
│   │   └── admin/
│   │       └── admin_screen.dart
│   │
│   └── widgets/                      # Общие виджеты
│       ├── persona_selector.dart
│       ├── tag_selector.dart
│       ├── xp_bar.dart
│       ├── streak_indicator.dart
│       ├── session_timer.dart
│       ├── ocr_result_viewer.dart
│       └── markdown_viewer.dart
│
└── utils/
    ├── camera_helper.dart
    ├── image_compressor.dart
    └── formatters.dart
```

### 6.2 Экраны Flutter приложения

| Экран | Описание | Priority |
|-------|----------|----------|
| SplashScreen | Проверка авторизации | P0 |
| LoginScreen | Вход device_id/email | P0 |
| MainMenuScreen | Главное меню | P0 |
| ProblemListScreen | Список задач | P0 |
| ProblemDetailScreen | Детали задачи | P0 |
| SolutionSessionScreen | Интерактивная сессия | P0 |
| SolutionFinalizeScreen | Завершение решения | P0 |
| CameraScreen | Фото условий/решений | P0 |
| StatisticsScreen | Статистика и прогресс | P1 |
| LibraryScreen | Библиотека контента | P1 |
| ConceptAnalysisScreen | Анализ концепций | P1 |
| BillingScreen | Баланс и пополнение | P1 |
| ProfileScreen | Профиль пользователя | P1 |
| AdminScreen | Админка | P2 |

### 6.3 Зависимости Flutter (pubspec.yaml)

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  flutter_riverpod: ^2.4.0
  
  # Navigation
  go_router: ^12.0.0
  
  # HTTP Client
  dio: ^5.4.0
  
  # Secure Storage
  flutter_secure_storage: ^9.0.0
  
  # Camera & Images
  camera: ^0.10.5
  image_picker: ^1.0.4
  image: ^4.1.0
  
  # Markdown & Math
  flutter_markdown: ^0.6.18
  math_keyboard: ^0.2.1
  
  # UI Components
  flutter_animate: ^4.3.0
  shimmer: ^3.0.0
  cached_network_image: ^3.3.0
  
  # Charts
  fl_chart: ^0.66.0
  
  # Utils
  device_info_plus: ^9.1.0
  uuid: ^4.2.1
  intl: ^0.18.1
  
  # URL Launcher (для оплаты)
  url_launcher: ^6.2.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  build_runner: ^2.4.0
  json_serializable: ^6.7.0
```

### 6.4 Этапы разработки

#### Этап 1: Foundation (P0) — 2 недели
- [ ] Настройка проекта и структуры
- [ ] API клиент с Dio и интерцепторами
- [ ] Secure Storage для токенов
- [ ] Авторизация (device_login)
- [ ] Базовая навигация (GoRouter)

#### Этап 2: Core Features (P0) — 3 недели
- [ ] Список источников и задач
- [ ] Детали задачи
- [ ] Начало решения (create_solution)
- [ ] Интерактивная сессия с таймером
- [ ] Завершение решения с оценками
- [ ] Запись сессий

#### Этап 3: Camera & OCR (P0) — 1 неделя
- [ ] Интеграция камеры
- [ ] Загрузка изображений
- [ ] OCR распознавание
- [ ] Просмотр результата OCR

#### Этап 4: Gamification & Stats (P1) — 1 неделя
- [ ] Экран статистики
- [ ] Графики активности (fl_chart)
- [ ] XP, сердца, стрик

#### Этап 5: Artifacts (P1) — 1 неделя
- [ ] Озарения (epiphanies)
- [ ] Вопросы (questions)
- [ ] Подсказки (hints)
- [ ] AI генерация ответов

#### Этап 6: Concepts & Billing (P1) — 1 неделя
- [ ] Анализ концепций задач
- [ ] Трейс навыков решений
- [ ] Баланс и пополнение

#### Этап 7: Polish & Admin (P2) — 1 неделя
- [ ] Анимации (flutter_animate)
- [ ] Shimmer эффекты
- [ ] Админка
- [ ] Обработка ошибок
- [ ] Offline режим (опционально)

---

## 7. Особенности мобильного UX

### 7.1 Интерактивная сессия на мобильном

Вместо текстовых команд — FAB (Floating Action Button) и Bottom Sheet:

```
┌─────────────────────────────────────┐
│ 🚀 СЕССИЯ: Задача #123              │
│ ⏱ 00:15:32                         │
├─────────────────────────────────────┤
│                                     │
│     [Область для контента]          │
│                                     │
│                                     │
├─────────────────────────────────────┤
│  [💡 Озарение]  [❓ Вопрос]         │
│  [🆘 Подсказка] [👁 Решение]        │
├─────────────────────────────────────┤
│         [🏁 ЗАВЕРШИТЬ]              │
└─────────────────────────────────────┘
```

### 7.2 Камера для фото задач

```
┌─────────────────────────────────────┐
│           📸 КАМЕРА                 │
├─────────────────────────────────────┤
│                                     │
│     [Предпросмотр камеры]           │
│                                     │
│                                     │
├─────────────────────────────────────┤
│  [📷 Сфоткать]  [📁 Галерея]        │
│                                     │
│  Выберите тип:                      │
│  ○ Условие задачи                   │
│  ○ Решение                          │
│  ○ Контекст вопроса                 │
└─────────────────────────────────────┘
```

### 7.3 Выбор AI персоны

```
┌─────────────────────────────────────┐
│       🤔 КОГО СПРОСИТЬ?             │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │ 🐱 Кот Базис                    │ │
│ │ Бесплатно • Может лениться      │ │
│ │ Осталось: 3/5 запросов          │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 🧹 Петрович                     │ │
│ │ 2 ₽ • Быстро • Gemini Flash     │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 🧐 Лежандр                      │ │
│ │ 10 ₽ • Точно • Gemini Pro       │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## 8. API Endpoints Summary

```
AUTH
├── POST   /auth/device-register     # Анонимный вход
├── POST   /auth/login               # Email вход
└── POST   /auth/register            # Регистрация

USERS
├── GET    /users/me                 # Профиль
└── PATCH  /users/me/convert         # Конвертация анонимного

PROBLEMS
├── GET    /problems                 # Список задач
├── POST   /problems                 # Создать задачу
├── GET    /problems/{id}            # Детали задачи
└── PATCH  /problems/{id}            # Обновить задачу

SOLUTIONS
├── GET    /solutions                # Список решений
├── POST   /solutions                # Начать решение
├── GET    /solutions/{id}           # Детали решения
└── PATCH  /solutions/{id}           # Завершить решение

SESSIONS
└── POST   /sessions                 # Записать сессию

EPIPHANIES
└── POST   /epiphanies               # Создать озарение

QUESTIONS
├── GET    /questions/by-solution/{id}
├── POST   /questions
├── GET    /questions/{id}
├── PATCH  /questions/{id}
└── POST   /questions/{id}/generate

HINTS
├── POST   /hints/draft
├── GET    /hints/by-solution/{id}
├── POST   /hints/{id}/generate
└── PATCH  /hints/{id}

UPLOADS
└── POST   /uploads/{category}/{id}  # Загрузка изображений

CONTENT (OCR)
├── POST   /content/process-image/problem/{id}
└── POST   /content/process-image/solution/{id}

CONCEPTS
├── POST   /concepts/analyze/problem/{id}
├── POST   /concepts/analyze/solution/{id}
└── POST   /concepts/deduplicate

BILLING
├── GET    /billing/balance
└── POST   /billing/top-up

GAMIFICATION
├── GET    /gamification/me
└── GET    /gamification/activity/daily

SOURCES
├── GET    /sources
└── GET    /tags
```

---

## 9. Следующие шаги

1. **Создать Flutter проект** с базовой структурой
2. **Реализовать API клиент** с авторизацией
3. **Разработать ключевые экраны** (главное меню, задачи, сессия)
4. **Интегрировать камеру** для фото
5. **Добавить геймификацию** и статистику
6. **Стилизовать под Material 3** с красивыми анимациями

---

*Документ создан на основе анализа файлов:*
- `KODA.md` — документация проекта
- `mv_run_client.py` — точка входа
- `mv_api.py` — API клиент
- `mv_screens.py` — UI экраны
- `mv_context.py` — системный контекст
