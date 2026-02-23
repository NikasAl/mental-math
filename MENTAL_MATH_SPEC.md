# Mental Math Trainer — Спецификация проекта

## 1. Цель проекта

Создать тренажёр навыков мышления, который помогает пользователю:
- Уменьшить зависимость от черновика при решении задач
- Развить способность делать расчёты и преобразования в уме
- Прогрессивно повышать сложность от элементарной арифметики до задач уровня Сканави/Демидовича

**Ключевой принцип**: Не скорость, а качество представления преобразований в уме. Пользователь должен научиться "видеть" путь решения и удерживать промежуточные результаты в рабочей памяти.

---

## 2. Уровни сложности

### Уровень 1: Элементарная арифметика
- Сложение/вычитание двузначных чисел
- Умножение/деление на однозначное число
- Примеры: `47 + 38`, `156 - 89`, `24 × 7`

### Уровень 2: Устный счёт
- Умножение двузначных чисел
- Деление с остатком
- Простые дроби
- Примеры: `23 × 17`, `157 ÷ 12`, `3/4 + 5/6`

### Уровень 3: Алгебраические преобразования
- Раскрытие скобок
- Формулы сокращённого умножения
- Упрощение выражений
- Примеры: `(a + b)²`, `(x - 3)(x + 5)`, `a² - b²`

### Уровень 4: Уравнения и неравенства
- Линейные уравнения
- Квадратные уравнения
- Системы уравнений
- Примеры: `3x + 7 = 22`, `x² - 5x + 6 = 0`

### Уровень 5: Функции и графики
- Исследование функций
- Построение графиков в уме
- Производные

### Уровень 6: Тригонометрия
- Тригонометрические тождества
- Преобразование выражений
- Примеры: `sin²α + cos²α`, `sin(α + β)`

### Уровень 7: Логарифмы и степени
- Свойства логарифмов
- Показательные уравнения
- Примеры: `log₂8 + log₂4`, `2^x = 16`

### Уровень 8: Интегралы и производные
- Табличные интегралы
- Правила дифференцирования
- Примеры: `∫x²dx`, `d/dx(sin x)`

### Уровень 9: Сложные алгебраические выражения
- Многоэтажные дроби
- Радикалы
- Примеры как в задании:
$$\left( \frac{(1+a^{-1/2})^{1/6}}{(a^{1/2}+1)^{-1/3}} - \frac{(a^{1/2}-1)^{1/3}}{(1-a^{-1/2})^{-1/6}} \right)^{-2} \cdot \frac{a^{1/12}}{\sqrt{a}+\sqrt{a-1}}$$

### Уровень 10: Олимпиадные задачи
- Задачи уровня Сканави, Демидовича
- Нестандартные методы
- Комбинация нескольких тем

---

## 3. Методика повышения сложности

### Принципы:

1. **Адаптивность**: Система подбирает задачи на грани возможностей пользователя (Zone of Proximal Development)

2. **Микро-прогрессия**: Каждый уровень делится на подуровни (1.1, 1.2, ..., 1.10)

3. **Повторение с вариациями**: Одна и та же задача в разных формулировках

4. **Разбор ошибок**: После ошибки — детальный разбор и похожая задача

5. **Дыхательные паузы**: Перед сложной задачей — подготовка и визуализация

### Метрики прогресса:

- **Точность**: % правильно решённых задач
- **Глубина**: сколько шагов решения удерживает в уме
- **Стабильность**: меньше ошибок при одинаковой сложности
- **Скорость** (вторична): время на задачу

---

## 4. Функциональность

### 4.1 Режимы тренировки

**Режим "Свободная тренировка"**
- Выбор уровня сложности
- Бесконечная генерация задач
- Без давления времени

**Режим "Дневной вызов"**
- 5 задач подобранных под текущий уровень
- Отслеживание стрика
- Награды за серию

**Режим "Экзамен"**
- Задачи нескольких уровней
- Жёсткие критерии оценки
- Сертификат уровня

**Режим "Спарринг"**
- Соревнование с другим пользователем
- Одинаковые задачи
- Кто точнее и быстрее

### 4.2 Интерфейс решения

**Ключевая механика**: Пользователь вводит только конечный ответ, но может отметить сколько шагов сделал в уме vs на бумаге.

Для каждого шага решения:
1. **Полностью в уме** — максимальный XP
2. **С подглядыванием в черновик** — часть XP
3. **С полной записью** — минимум XP

**Помощник**: Кнопка "Подсказка" — AI подсказывает следующий шаг, но снижает награду.

### 4.3 Идеологический модуль (AI-наставник)

AI-наставник объясняет:
- Как правильно думать над задачей этого типа
- Какие техники использовать
- Типичные ошибки и как их избежать
- Отвечает на вопросы пользователя

**Персоны наставника**:
- 🎓 **Академик** — строгий, академичный стиль
- 🧙 **Мудрец** — метафоры и аналогии
- 🏋️ **Тренер** — мотивация и поддержка

---

## 5. Архитектура сервера

### 5.1 Общая схема

Проект состоит из двух независимых компонентов:
- **Frontend** — Next.js 15 приложение (клиент)
- **Backend** — отдельный FastAPI сервер (API)

Сервер разрабатывается с нуля, используя технологии проверенные в проекте Лежандр (KODA).

### 5.2 Технологический стек сервера

```
Backend (FastAPI + Python):
├── FastAPI — веб-фреймворк
├── SQLAlchemy 2.0 — ORM (async)
├── PostgreSQL — база данных
├── Alembic — миграции
├── Pydantic v2 — валидация
├── python-jose — JWT токены
├── passlib — хеширование паролей
├── OpenRouter API — LLM для генерации задач и подсказок
```

### 5.3 Структура проекта сервера

```
mental_math_server/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Точка входа FastAPI
│   ├── config.py               # Конфигурация (env)
│   ├── database.py             # Подключение к БД
│   ├── models/                 # SQLAlchemy модели
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── session.py
│   │   └── progress.py
│   ├── schemas/                # Pydantic схемы
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── session.py
│   ├── routers/                # API эндпоинты
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   ├── sessions.py
│   │   ├── progress.py
│   │   └── ai.py
│   ├── services/               # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── task_generator.py   # Генерация задач
│   │   ├── answer_validator.py # Проверка ответов
│   │   ├── level_manager.py    # Управление уровнями
│   │   └── ai_mentor.py        # AI-наставник
│   └── utils/
│       ├── __init__.py
│       ├── security.py         # JWT, хеширование
│       └── latex_parser.py     # Парсинг LaTeX
├── alembic/                    # Миграции БД
├── tests/
├── requirements.txt
└── venv
```

### 5.4 API Эндпоинты

#### Авторизация
```
POST /api/v1/auth/accunt-login  — Регистрация/вход по account_key
POST /api/v1/auth/login            — Вход по email/паролю
POST /api/v1/auth/register         — Регистрация с email
POST /api/v1/auth/refresh          — Обновление токена
GET  /api/v1/auth/me               — Текущий пользователь
```

#### Задачи
```
GET  /api/v1/tasks                 — Список задач (с фильтрами)
GET  /api/v1/tasks/{id}            — Конкретная задача
POST /api/v1/tasks/generate        — Генерация задачи по уровню
POST /api/v1/tasks/validate        — Проверка ответа
GET  /api/v1/tasks/levels          — Список уровней сложности
GET  /api/v1/tasks/topics          — Список тем по уровням
```

#### Сессии и прогресс
```
POST /api/v1/sessions              — Запись сессии решения
GET  /api/v1/sessions              — История сессий пользователя
GET  /api/v1/progress              — Прогресс пользователя
GET  /api/v1/progress/stats        — Статистика по периодам
GET  /api/v1/progress/streak       — Информация о стрике
```

#### AI-функции
```
POST /api/v1/ai/hint               — Получить подсказку к задаче
POST /api/v1/ai/explain            — Объяснить решение
POST /api/v1/ai/question           — Задать вопрос наставнику
POST /api/v1/ai/analyze-error      — Анализ ошибки
```

#### Геймификация
```
GET  /api/v1/gamification/me       — XP, уровень, достижения
GET  /api/v1/gamification/activity — Активность по дням
POST /api/v1/gamification/daily    — Дневной вызов
GET  /api/v1/gamification/achievements — Достижения пользователя
```

### 5.5 Модели данных (SQLAlchemy)

```python
# models/user.py
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str | None] = mapped_column(String, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String, unique=True)
    hashed_password: Mapped[str | None]
    account_key: Mapped[str | None] = mapped_column(String, unique=True, index=True)
    is_anonymous: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    
    # Relationships
    progress: Mapped["UserProgress"] = relationship(back_populates="user")
    sessions: Mapped[List["Session"]] = relationship(back_populates="user")

# models/task.py
class Task(Base):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[int] = mapped_column(SmallInteger)  # 1-10
    sub_level: Mapped[int] = mapped_column(SmallInteger)  # 1-10
    topic: Mapped[str] = mapped_column(String(100))
    expression: Mapped[str] = mapped_column(Text)  # LaTeX
    answer: Mapped[str] = mapped_column(String(500))
    solution_steps: Mapped[list] = mapped_column(JSON)  # ["шаг1", "шаг2", ...]
    hints: Mapped[list] = mapped_column(JSON)
    difficulty: Mapped[int] = mapped_column(SmallInteger)  # 1-100
    is_ai_generated: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

# models/session.py
class Session(Base):
    __tablename__ = "sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_answer: Mapped[str] = mapped_column(String(500))
    is_correct: Mapped[bool]
    mental_steps: Mapped[int] = mapped_column(SmallInteger)  # шагов в уме
    written_steps: Mapped[int] = mapped_column(SmallInteger)  # на бумаге
    time_seconds: Mapped[int] = mapped_column(Integer)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    hints_used: Mapped[int] = mapped_column(SmallInteger, default=0)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="sessions")
    task: Mapped["Task"] = relationship()

# models/progress.py
class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    current_level: Mapped[int] = mapped_column(SmallInteger, default=1)
    level_progress: Mapped[int] = mapped_column(SmallInteger, default=0)  # 0-100
    total_xp: Mapped[int] = mapped_column(Integer, default=0)
    total_tasks: Mapped[int] = mapped_column(Integer, default=0)
    correct_tasks: Mapped[int] = mapped_column(Integer, default=0)
    streak_current: Mapped[int] = mapped_column(SmallInteger, default=0)
    streak_max: Mapped[int] = mapped_column(SmallInteger, default=0)
    last_activity: Mapped[datetime | None]
    strengths: Mapped[list] = mapped_column(JSON, default=list)
    weaknesses: Mapped[list] = mapped_column(JSON, default=list)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="progress")

class Achievement(Base):
    __tablename__ = "achievements"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(10))  # emoji
    xp_reward: Mapped[int] = mapped_column(Integer)
    condition_type: Mapped[str] = mapped_column(String(50))
    condition_value: Mapped[int] = mapped_column(Integer)

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"))
    earned_at: Mapped[datetime] = mapped_column(default=func.now())
```

### 5.6 Сервис генерации задач

```python
# services/task_generator.py
class TaskGenerator:
    """Генерация задач по уровню сложности"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.templates = self._load_templates()
    
    async def generate(self, level: int, sub_level: int, topic: str | None = None) -> Task:
        """Генерация задачи с заданными параметрами"""
        
        if level <= 3:
            # Для простых уровней — шаблонная генерация
            return self._generate_template(level, sub_level, topic)
        else:
            # Для сложных уровней — AI генерация
            return await self._generate_ai(level, sub_level, topic)
    
    def _generate_template(self, level: int, sub_level: int, topic: str | None) -> Task:
        """Генерация по шаблонам (уровни 1-3)"""
        # Примеры шаблонов для уровня 1:
        # {a} + {b} = ? где a, b подбираются по sub_level
        pass
    
    async def _generate_ai(self, level: int, sub_level: int, topic: str | None) -> Task:
        """AI генерация сложных задач (уровни 4-10)"""
        prompt = self._build_generation_prompt(level, sub_level, topic)
        response = await self.llm.generate(prompt)
        return self._parse_response(response)

# services/answer_validator.py
class AnswerValidator:
    """Проверка ответов пользователя"""
    
    def validate(self, user_answer: str, correct_answer: str, task_type: str) -> bool:
        """Сравнение ответов с учётом формата"""
        
        # Нормализация
        user = self._normalize(user_answer)
        correct = self._normalize(correct_answer)
        
        # Прямое сравнение
        if user == correct:
            return True
        
        # Числовое сравнение (с допуском)
        if self._is_numeric(user) and self._is_numeric(correct):
            return abs(float(user) - float(correct)) < 0.001
        
        # Сравнение выражений (a+b vs b+a)
        if task_type == "expression":
            return self._compare_expressions(user, correct)
        
        return False
```

### 5.7 Сервис AI-наставника

```python
# services/ai_mentor.py
class AIMentor:
    """Идеологический модуль — AI-наставник"""
    
    PERSONAS = {
        "academic": "🎓 Академик — строгий, академичный стиль",
        "sage": "🧙 Мудрец — метафоры и аналогии", 
        "coach": "🏋️ Тренер — мотивация и поддержка"
    }
    
    async def get_hint(self, task: Task, step: int, persona: str) -> str:
        """Получить подсказку для текущего шага"""
        prompt = f"""
        Задача: {task.expression}
        Правильный ответ: {task.answer}
        Шаги решения: {task.solution_steps}
        
        Пользователь застрял на шаге {step}.
        Дай подсказку в стиле {self.PERSONAS.get(persona, 'academic')}.
        Не раскрывай полностью следующий шаг, только направь.
        """
        return await self.llm.generate(prompt)
    
    async def explain_solution(self, task: Task, persona: str) -> str:
        """Объяснить полное решение"""
        prompt = f"""
        Задача: {task.expression}
        Шаги решения: {task.solution_steps}
        
        Объясни решение подробно в стиле {self.PERSONAS.get(persona, 'academic')}.
        Объясни почему каждый шаг делается именно так.
        """
        return await self.llm.generate(prompt)
    
    async def analyze_error(self, task: Task, user_answer: str, persona: str) -> str:
        """Анализ ошибки пользователя"""
        prompt = f"""
        Задача: {task.expression}
        Правильный ответ: {task.answer}
        Ответ пользователя: {user_answer}
        
        Проанализируй ошибку в стиле {self.PERSONAS.get(persona, 'academic')}.
        Опиши возможный ход мыслей, который привёл к ошибке.
        Дай совет как избежать подобных ошибок.
        """
        return await self.llm.generate(prompt)
    
    async def answer_question(self, question: str, context: dict, persona: str) -> str:
        """Ответ на вопрос пользователя"""
        prompt = f"""
        Контекст: пользователь решает задачу уровня {context.get('level')}
        Тема: {context.get('topic')}
        
        Вопрос пользователя: {question}
        
        Ответь в стиле {self.PERSONAS.get(persona, 'academic')}.
        Будь полезным и поощряй самостоятельное мышление.
        """
        return await self.llm.generate(prompt)
```

---

## 6. Технический стек клиента (Frontend)

```
Frontend (Next.js 15):
├── Next.js 15 App Router
├── TypeScript 5
├── TailwindCSS 3 + shadcn/ui
├── Zustand — состояние
├── React Hook Form + Zod — формы
├── KaTeX — рендеринг LaTeX формул
├── SWR или TanStack Query — запросы к API
└── next-pwa (опционально) — оффлайн поддержка
```

### Структура клиента

```
mental_math_client/
├── src/
│   ├── app/                     # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx             # Главная
│   │   ├── train/
│   │   │   └── page.tsx         # Режим тренировки
│   │   ├── daily/
│   │   │   └── page.tsx         # Дневной вызов
│   │   ├── stats/
│   │   │   └── page.tsx         # Статистика
│   │   └── profile/
│   │       └── page.tsx         # Профиль
│   ├── components/
│   │   ├── ui/                  # shadcn компоненты
│   │   ├── math/                # Компоненты для формул
│   │   │   ├── FormulaDisplay.tsx
│   │   │   └── FormulaInput.tsx
│   │   ├── task/                # Компоненты задач
│   │   │   ├── TaskCard.tsx
│   │   │   ├── AnswerInput.tsx
│   │   │   ├── SolutionSteps.tsx
│   │   │   └── HintButton.tsx
│   │   └── gamification/
│   │       ├── XPDisplay.tsx
│   │       ├── LevelProgress.tsx
│   │       └── StreakCounter.tsx
│   ├── lib/
│   │   ├── api.ts               # API клиент
│   │   ├── auth.ts              # Авторизация
│   │   └── latex.ts             # Утилиты для LaTeX
│   ├── hooks/
│   │   ├── useTask.ts
│   │   ├── useProgress.ts
│   │   └── useStreak.ts
│   └── store/
│       ├── userStore.ts
│       └── settingsStore.ts
├── public/
├── package.json
└── tailwind.config.ts
```

---

## 7. Структура данных

### MentalTask (Задача для устного счёта)
```typescript
interface MentalTask {
  id: number;
  level: number;          // 1-10
  subLevel: number;       // 1-10
  topic: string;          // "арифметика", "алгебра", ...
  expression: string;     // LaTeX формула
  answer: string;         // Правильный ответ
  solutionSteps: string[];// Шаги решения для разбора
  hints: string[];        // Подсказки
  difficulty: number;     // Внутренняя сложность 1-100
}
```

### MentalSession (Сессия тренировки)
```typescript
interface MentalSession {
  id: number;
  userId: number;
  taskId: number;
  userAnswer: string;
  isCorrect: boolean;
  mentalSteps: number;    // Сколько шагов в уме
  writtenSteps: number;   // Сколько на бумаге
  timeSeconds: number;
  xpEarned: number;
  createdAt: Date;
}
```

### UserProgress (Прогресс пользователя)
```typescript
interface UserProgress {
  userId: number;
  currentLevel: number;
  levelProgress: number;  // 0-100% до следующего уровня
  totalTasks: number;
  correctRate: number;    // % правильных
  streak: number;
  strengths: string[];    // Сильные темы
  weaknesses: string[];   // Слабые темы
}
```

---

## 8. План разработки

### Фаза 1: MVP (2 недели)
- [ ] Базовый UI с отображением формул
- [ ] 3 уровня сложности (1-3)
- [ ] Генерация задач локально
- [ ] Ввод ответа и проверка
- [ ] Простой счётчик XP

### Фаза 2: Интеграция (2 недели)
- [ ] Авторизация через Лежандр
- [ ] Сохранение прогресса на сервер
- [ ] Синхронизация между устройствами
- [ ] Базовый идеологический модуль

### Фаза 3: Геймификация (2 недели)
- [ ] Дневной вызов
- [ ] Система уровней и стриков
- [ ] Достижения
- [ ] Статистика и графики

### Фаза 4: Продвинутые уровни (4 недели)
- [ ] Уровни 4-10
- [ ] AI-генерация сложных задач
- [ ] Адаптивная сложность
- [ ] Разбор ошибок

### Фаза 5: Социальные функции (2 недели)
- [ ] Режим спарринга
- [ ] Рейтинги
- [ ] Друзья

---

## 9. Примеры UI

### Главный экран:
```
┌─────────────────────────────────┐
│ 🧠 Mental Math Trainer          │
│                                 │
│ Уровень: 3 ▓▓▓▓▓▓░░░░ 62%       │
│ Стрик: 🔥 7 дней                 │
│                                 │
│ ┌─────────────────────────────┐ │
│ │         47 × 38 = ?         │ │
│ │                             │ │
│ │    [Подсказка]  [Решение]   │ │
│ │                             │ │
│ │    Ответ: [___________]     │ │
│ │                             │ │
│ │    Шагов в уме: ○1 ○2 ○3 ●4 │ │
│ │    На бумаге:  ●0 ○1 ○2     │ │
│ │                             │ │
│ │         [Проверить]         │ │
│ └─────────────────────────────┘ │
│                                 │
│ 📊 Сегодня: 12 задач, 92%       │
└─────────────────────────────────┘
```

### Экран разбора:
```
┌─────────────────────────────────┐
│ ✅ Правильно! +15 XP            │
│                                 │
│ 47 × 38 = ?                     │
│                                 │
│ Ваш путь:                       │
│ 1. 47 × 38 = 47 × 40 - 47 × 2  │
│ 2. 47 × 40 = 1880              │
│ 3. 47 × 2 = 94                 │
│ 4. 1880 - 94 = 1786            │
│                                 │
│ 💡 Совет: Умножение на 40       │
│    проще чем на 38             │
│                                 │
│ [Следующая задача]              │
└─────────────────────────────────┘
```

---

## 10. Ключевые метрики успеха

1. **Retention D7** > 40% — пользователи возвращаются
2. **Средняя сессия** > 10 минут
3. **Прогресс уровня** — минимум 1 уровень за месяц регулярного использования
4. **NPS** > 50 — готовы рекомендовать

---

## Приложения

### A. Примеры задач по уровням

**Уровень 1**:
- `7 + 8 = ?` (15)
- `23 - 9 = ?` (14)
- `6 × 7 = ?` (42)

**Уровень 3**:
- `(a + b)² - a² - b² = ?` (2ab)
- `x² - 9 = ?` ((x-3)(x+3))

**Уровень 5**:
- `Минимум функции x² - 4x + 5` (x=2, y=1)
- `Производная x³` (3x²)

**Уровень 9**:
- Комплексные выражения с радикалами и степенями

### B. Ресурсы

- [Сканави — Сборник задач](https://ru.wikipedia.org/wiki/Сканави)
- [Демидович — Задачи и упражнения](https://ru.wikipedia.org/wiki/Демидович)
- [KaTeX](https://katex.org/) — рендеринг формул
- [OpenRouter API](https://openrouter.ai/) — LLM для подсказок
