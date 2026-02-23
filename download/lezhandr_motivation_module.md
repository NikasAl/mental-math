# Лежандр — Motivation Module
## Модуль мотивации для Flutter приложения

---

## 1. Концепция и назначение

### 1.1 Философия модуля

Модуль мотивации — это система психологической поддержки пользователя, которая:

- **Напоминает о ценности** решения задач в моменты сомнений
- **Поддерживает в трудностях** при длительных сессиях
- **Празднует успехи** при завершении задач
- **Строит долгосрочную мотивацию** через осознание пользы обучения

### 1.2 Принципы показа

| Принцип | Описание |
|---------|----------|
| **Не навязчивость** | Тексты появляются естественно, не прерывая работу |
| **Контекстность** | Текст соответствует текущей ситуации пользователя |
| **Разнообразие** | Избегаем повторений, используем рандомизацию |
| **Персонализация** | Учитываем историю пользователя (стрик, сложность задач) |

### 1.3 Точки касания (Touchpoints)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MOTIVATION TOUCHPOINTS MAP                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. ONBOARDING (Первый запуск)                                              │
│     └── Показ миссии приложения                                             │
│                                                                             │
│  2. HOME SCREEN (При открытии)                                              │
│     ├── Утреннее приветствие (6:00-12:00)                                  │
│     ├── Дневное поощрение (12:00-18:00)                                    │
│     └── Вечерняя поддержка (18:00-24:00)                                   │
│                                                                             │
│  3. SESSION START (Начало решения)                                          │
│     ├── При выборе сложной задачи                                          │
│     ├── При продолжении прерванного решения                                │
│     └── При длительном перерыве (не решал > 3 дней)                        │
│                                                                             │
│  4. SESSION IN PROGRESS (В процессе)                                        │
│     ├── Через 15 минут без перерыва → "Отдых важен"                        │
│     ├── Через 30 минут без прогресса → "Не сдавайся"                       │
│     └── При запросе подсказки → "Это нормально"                            │
│                                                                             │
│  5. SESSION END (Завершение)                                                │
│     ├── Успешное завершение → Поздравление + XP                            │
│     ├── Прерывание → Поддержка                                              │
│     └── После сложной задачи → "Ты справился!"                             │
│                                                                             │
│  6. STREAK (Стрик)                                                          │
│     ├── Новый рекорд стрика → Особое поздравление                          │
│     ├── Риск потери стрика → "Не прерывай цепь"                            │
│     └── Восстановление стрика → "С возвращением"                           │
│                                                                             │
│  7. STATISTICS (Экран статистики)                                           │
│     ├── Достижение новой вехи (100 задач, 1000 XP)                         │
│     └── Еженедельный дайджест                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Категории мотивационных текстов

### 2.1 Структура категории

```dart
enum MotivationCategory {
  thinking,        // Про развитие мышления
  practical,       // Про практическую пользу
  satisfaction,    // Про удовлетворение от решения
  career,          // Про будущее и карьеру
  perseverance,    // Про преодоление трудностей
  energetic,       // Короткие и энергичные
  quotes,          // Цитаты великих людей
  session,         // Во время сессии
  streak,          // Про стрик
  achievements,    // При достижениях
}
```

### 2.2 База текстов

#### Категория: THINKING (Развитие мышления)

```json
[
  {
    "id": "thinking_01",
    "text": "Каждая решенная задача — это гантель для твоего мозга: чем больше поднимаешь, тем сильнее становишься",
    "author": null,
    "tags": ["brain", "strength", "growth"]
  },
  {
    "id": "thinking_02", 
    "text": "Математика учит не только считать, но думать. Физика — не формулы, а видение мира глазами ученого",
    "author": null,
    "tags": ["math", "physics", "vision"]
  },
  {
    "id": "thinking_03",
    "text": "Решая задачи сегодня, ты программируешь свой мозг на успех в любой сфере завтра",
    "author": null,
    "tags": ["future", "success", "programming"]
  },
  {
    "id": "thinking_04",
    "text": "Математика — не про знание формул, а про понимание их происхождения. Выводи их сам!",
    "author": null,
    "tags": ["formulas", "understanding", "discovery"]
  },
  {
    "id": "thinking_05",
    "text": "Только через задачи можно по-настоящему понять математику, физику и природу реальности",
    "author": null,
    "tags": ["reality", "understanding", "nature"]
  },
  {
    "id": "thinking_06",
    "text": "Математику уже затем учить надо, что она ум в порядок приводит",
    "author": "М.В. Ломоносов",
    "tags": ["classic", "mind", "order"]
  }
]
```

#### Категория: PRACTICAL (Практическая польза)

```json
[
  {
    "id": "practical_01",
    "text": "Знания из учебника останутся там же. А навыки, полученные при решении задач, пригодятся в реальной жизни каждый день",
    "author": null,
    "tags": ["skills", "real_life", "practice"]
  },
  {
    "id": "practical_02",
    "text": "Не знаешь, зачем тебе интегралы? Начни делать вещи, и они сами начнут решаться",
    "author": null,
    "tags": ["integrals", "action", "understanding"]
  },
  {
    "id": "practical_03",
    "text": "Каждая задача — это шаг к тому, чтобы понимать, как устроен мир вокруг тебя",
    "author": null,
    "tags": ["world", "understanding", "steps"]
  },
  {
    "id": "practical_04",
    "text": "Невозможно применить на практике то, что не знаешь. Узнай математику — и увидишь её применения",
    "author": null,
    "tags": ["practice", "knowledge", "application"]
  },
  {
    "id": "practical_05",
    "text": "Задачи — это практическое знание. Теория без практики мертва",
    "author": null,
    "tags": ["theory", "practice", "knowledge"]
  }
]
```

#### Категория: SATISFACTION (Удовлетворение)

```json
[
  {
    "id": "satisfaction_01",
    "text": "Помнишь чувство, когда наконец-то решил сложную задачу? Это не просто ответ, это доказательство твоей силы",
    "author": null,
    "tags": ["achievement", "strength", "feeling"]
  },
  {
    "id": "satisfaction_02",
    "text": "Самый сладкий момент в учебе — это когда после долгих попыток лампочка наконец загорается над головой",
    "author": null,
    "tags": ["eureka", "success", "effort"]
  },
  {
    "id": "satisfaction_03",
    "text": "Ты не просто решаешь задачи — ты собираешь пазл своего образования, и каждая деталь важна",
    "author": null,
    "tags": ["puzzle", "education", "importance"]
  },
  {
    "id": "satisfaction_04",
    "text": "Чувство, когда понимаешь, КАК решать — лучше любого кофе. Заряжает на весь день!",
    "author": null,
    "tags": ["energy", "understanding", "motivation"]
  }
]
```

#### Категория: CAREER (Будущее и карьера)

```json
[
  {
    "id": "career_01",
    "text": "Сегодня ты решаешь задачи в тетради, завтра — реальные проблемы в жизни. Навыки те же",
    "author": null,
    "tags": ["future", "skills", "problems"]
  },
  {
    "id": "career_02",
    "text": "Хороший специалист в любой области — это человек, который умеет решать задачи. Начни с математических",
    "author": null,
    "tags": ["specialist", "skills", "professional"]
  },
  {
    "id": "career_03",
    "text": "Диплом откроет двери, а умение решать сложные задачи сделает тебя незаменимым",
    "author": null,
    "tags": ["career", "value", "indispensable"]
  },
  {
    "id": "career_04",
    "text": "Инженеры, учёные, программисты — все они начали с решения задач. Твой путь начинается здесь",
    "author": null,
    "tags": ["career", "path", "profession"]
  }
]
```

#### Категория: PERSEVERANCE (Преодоление трудностей)

```json
[
  {
    "id": "perseverance_01",
    "text": "Самые сильные мышцы растут от тяжелых упражнений, а умные мозги — от сложных задач",
    "author": null,
    "tags": ["growth", "difficulty", "strength"]
  },
  {
    "id": "perseverance_02",
    "text": "Хорошая задача решается три дня и три ночи. Не торопись, думай глубоко",
    "author": null,
    "tags": ["patience", "depth", "thinking"]
  },
  {
    "id": "perseverance_03",
    "text": "Если задача кажется слишком сложной — отлично! Значит, ты на пути к настоящему росту",
    "author": null,
    "tags": ["growth", "challenge", "opportunity"]
  },
  {
    "id": "perseverance_04",
    "text": "Не бойся ошибок. Каждая ошибка в решении — это шаг к правильному ответу и твоему опыту",
    "author": null,
    "tags": ["mistakes", "learning", "experience"]
  },
  {
    "id": "perseverance_05",
    "text": "Время, потраченное на задачи — это знания, опыт и лучшая инвестиция в будущее, которую ты можешь сделать",
    "author": null,
    "tags": ["time", "investment", "future"]
  },
  {
    "id": "perseverance_06",
    "text": "Будь честен перед собой. Признай, если что-то не понимаешь — это первый шаг к пониманию",
    "author": null,
    "tags": ["honesty", "understanding", "growth"]
  }
]
```

#### Категория: ENERGETIC (Короткие и энергичные)

```json
[
  {
    "id": "energetic_01",
    "text": "Решил задачу — победил себя!",
    "author": null,
    "tags": ["victory", "self", "short"]
  },
  {
    "id": "energetic_02",
    "text": "Сегодняшние уравнения — завтрашние возможности",
    "author": null,
    "tags": ["equations", "opportunities", "future"]
  },
  {
    "id": "energetic_03",
    "text": "Одна задача — один шаг вперёд!",
    "author": null,
    "tags": ["progress", "steps", "action"]
  },
  {
    "id": "energetic_04",
    "text": "Твой мозг способен на большее. Докажи это!",
    "author": null,
    "tags": ["potential", "proof", "challenge"]
  },
  {
    "id": "energetic_05",
    "text": "Каждый гений начинал с простой задачи",
    "author": null,
    "tags": ["genius", "beginning", "inspiration"]
  }
]
```

#### Категория: QUOTES (Цитаты великих)

```json
[
  {
    "id": "quote_01",
    "text": "Математику уже затем учить надо, что она ум в порядок приводит",
    "author": "Михаил Ломоносов",
    "tags": ["classic", "mind", "russian"]
  },
  {
    "id": "quote_02",
    "text": "Вдохновение нужно в геометрии не меньше, чем в поэзии",
    "author": "Александр Пушкин",
    "tags": ["inspiration", "geometry", "poetry"]
  },
  {
    "id": "quote_03",
    "text": "Математика — это музыка разума",
    "author": "Джеймс Джозеф Сильвестр",
    "tags": ["music", "mind", "beautiful"]
  },
  {
    "id": "quote_04",
    "text": "Чистая математика — это место, где мы не знаем, о чём говорим, и не знаем, истинно ли то, что говорим",
    "author": "Бертран Рассел",
    "tags": ["philosophy", "truth", "humor"]
  },
  {
    "id": "quote_05",
    "text": "Математика — царица наук, арифметика — царица математики",
    "author": "Карл Фридрих Гаусс",
    "tags": ["queen", "science", "arithmetic"]
  },
  {
    "id": "quote_06",
    "text": "В каждой естественной науке заключено столько истины, сколько в ней математики",
    "author": "Иммануил Кант",
    "tags": ["truth", "science", "philosophy"]
  },
  {
    "id": "quote_07",
    "text": "Жизнь украшается двумя вещами: занятием математикой и её преподаванием",
    "author": "Симеон Дени Пуассон",
    "tags": ["life", "teaching", "passion"]
  }
]
```

#### Категория: SESSION (Во время сессии)

```json
[
  {
    "id": "session_01",
    "text": "Не получается? Это нормально. Самые интересные открытия рождаются из тупиков",
    "author": null,
    "tags": ["stuck", "discovery", "patience"],
    "trigger": "stuck_15min"
  },
  {
    "id": "session_02",
    "text": "Отдых — часть работы. Мозг обрабатывает информацию даже когда ты не думаешь о задаче",
    "author": null,
    "tags": ["rest", "brain", "processing"],
    "trigger": "session_30min"
  },
  {
    "id": "session_03",
    "text": "Подсказка — не слабость, а инструмент. Даже великие математики советовались с коллегами",
    "author": null,
    "tags": ["hint", "tool", "collaboration"],
    "trigger": "hint_requested"
  },
  {
    "id": "session_04",
    "text": "Ты уже потратил время. Теперь либо реши, либо извлеки урок. Оба варианта — победа",
    "author": null,
    "tags": ["time", "lesson", "victory"],
    "trigger": "session_long"
  },
  {
    "id": "session_05",
    "text": "Иногда лучший шаг — отступить и посмотреть на задачу свежим взглядом завтра",
    "author": null,
    "tags": ["rest", "perspective", "tomorrow"],
    "trigger": "session_very_long"
  }
]
```

#### Категория: STREAK (Про стрик)

```json
[
  {
    "id": "streak_01",
    "text": "7 дней подряд! Ты формируешь привычку, которая изменит твою жизнь",
    "author": null,
    "tags": ["streak", "habit", "milestone"],
    "condition": "streak_7"
  },
  {
    "id": "streak_02",
    "text": "30 дней! Это уже не привычка — это образ жизни",
    "author": null,
    "tags": ["streak", "lifestyle", "milestone"],
    "condition": "streak_30"
  },
  {
    "id": "streak_03",
    "text": "100 дней подряд! Ты входишь в топ 1% людей по упорству",
    "author": null,
    "tags": ["streak", "top", "dedication"],
    "condition": "streak_100"
  },
  {
    "id": "streak_04",
    "text": "Не прерывай цепь! Один день пропуска — и начинай сначала",
    "author": null,
    "tags": ["warning", "chain", "motivation"],
    "trigger": "streak_risk"
  },
  {
    "id": "streak_05",
    "text": "С возвращением! Новый стрик начинается сейчас, и он будет ещё длиннее",
    "author": null,
    "tags": ["return", "new_start", "encouragement"],
    "trigger": "streak_broken"
  },
  {
    "id": "streak_06",
    "text": "Огонь в твоём стрике горит уже {days} дней! Не дай ему погаснуть",
    "author": null,
    "tags": ["fire", "days", "continue"],
    "trigger": "streak_active"
  }
]
```

#### Категория: ACHIEVEMENTS (При достижениях)

```json
[
  {
    "id": "achievement_01",
    "text": "🎉 10 задач решено! Ты на верном пути!",
    "author": null,
    "tags": ["milestone", "beginner", "progress"],
    "condition": "tasks_10"
  },
  {
    "id": "achievement_02",
    "text": "🏆 50 задач! Ты уже опытный решатель!",
    "author": null,
    "tags": ["milestone", "experienced", "progress"],
    "condition": "tasks_50"
  },
  {
    "id": "achievement_03",
    "text": "⭐ 100 задач за плечами! Ты мастер своего дела!",
    "author": null,
    "tags": ["milestone", "master", "achievement"],
    "condition": "tasks_100"
  },
  {
    "id": "achievement_04",
    "text": "💎 500 задач! Ты в элите! Таких людей — единицы!",
    "author": null,
    "tags": ["elite", "rare", "legendary"],
    "condition": "tasks_500"
  },
  {
    "id": "achievement_05",
    "text": "🔥 1000 XP заработано! Твой мозг становится сильнее с каждой задачей!",
    "author": null,
    "tags": ["xp", "growth", "milestone"],
    "condition": "xp_1000"
  },
  {
    "id": "achievement_06",
    "text": "💡 Первое озарение! Эти моменты — золото учёного!",
    "author": null,
    "tags": ["epiphany", "first", "special"],
    "condition": "first_epiphany"
  },
  {
    "id": "achievement_07",
    "text": "📚 Ты прорешал задачи из 5 разных источников! Разносторонность — сила!",
    "author": null,
    "tags": ["sources", "diversity", "strength"],
    "condition": "sources_5"
  }
]
```

---

## 3. Архитектура модуля

### 3.1 Структура файлов

```
lib/
├── core/
│   └── motivation/
│       ├── motivation_module.dart         # Главный модуль
│       ├── motivation_engine.dart         # Логика выбора текстов
│       └── motivation_texts.dart          # База текстов
│
├── data/
│   └── motivation/
│       ├── models/
│       │   ├── motivation_text.dart       # Модель текста
│       │   └── motivation_context.dart    # Контекст показа
│       └── repositories/
│           └── motivation_repository.dart # Репозиторий
│
└── presentation/
    └── widgets/
        └── motivation/
            ├── motivation_card.dart       # Карточка с текстом
            ├── motivation_banner.dart     # Баннер в HomeScreen
            ├── motivation_popup.dart      # Popup при достижениях
            └── motivation_placeholder.dart # Placeholder при загрузке
```

### 3.2 Модели данных

```dart
// lib/data/motivation/models/motivation_text.dart

import 'package:json_annotation/json_annotation.dart';

part 'motivation_text.g.dart';

enum MotivationCategory {
  thinking,
  practical,
  satisfaction,
  career,
  perseverance,
  energetic,
  quotes,
  session,
  streak,
  achievements,
}

@JsonSerializable()
class MotivationText {
  final String id;
  final String text;
  final String? author;
  final List<String> tags;
  final MotivationCategory category;
  final String? trigger;      // Когда показывать
  final String? condition;    // Условие показа (например, streak_7)
  
  // Runtime fields
  final DateTime? lastShownAt;
  final int shownCount;

  MotivationText({
    required this.id,
    required this.text,
    this.author,
    required this.tags,
    required this.category,
    this.trigger,
    this.condition,
    this.lastShownAt,
    this.shownCount = 0,
  });

  factory MotivationText.fromJson(Map<String, dynamic> json) =>
      _$MotivationTextFromJson(json);
  
  Map<String, dynamic> toJson() => _$MotivationTextToJson(this);

  MotivationText copyWith({
    DateTime? lastShownAt,
    int? shownCount,
  }) {
    return MotivationText(
      id: id,
      text: text,
      author: author,
      tags: tags,
      category: category,
      trigger: trigger,
      condition: condition,
      lastShownAt: lastShownAt ?? this.lastShownAt,
      shownCount: shownCount ?? this.shownCount,
    );
  }
}
```

```dart
// lib/data/motivation/models/motivation_context.dart

enum TimeOfDay { morning, afternoon, evening, night }

enum SessionState {
  idle,
  starting,
  inProgress,
  stuck,        // Долго над одной задачей
  hintUsed,
  finishing,
}

class MotivationContext {
  final TimeOfDay timeOfDay;
  final SessionState sessionState;
  final int streakDays;
  final int tasksCompletedToday;
  final int totalTasksCompleted;
  final double totalXp;
  final int sessionDurationMinutes;
  final bool streakAtRisk;
  final bool justBrokeStreak;
  final bool isNewUser;
  final int daysSinceLastActivity;
  
  // Special conditions
  final bool firstEpiphany;
  final int sourcesUsed;
  final bool milestoneReached;
  final String? milestoneType; // 'tasks_100', 'xp_1000', etc.

  MotivationContext({
    required this.timeOfDay,
    required this.sessionState,
    this.streakDays = 0,
    this.tasksCompletedToday = 0,
    this.totalTasksCompleted = 0,
    this.totalXp = 0,
    this.sessionDurationMinutes = 0,
    this.streakAtRisk = false,
    this.justBrokeStreak = false,
    this.isNewUser = false,
    this.daysSinceLastActivity = 0,
    this.firstEpiphany = false,
    this.sourcesUsed = 0,
    this.milestoneReached = false,
    this.milestoneType,
  });

  factory MotivationContext.current({
    required SessionState sessionState,
    required int streakDays,
    required int tasksCompletedToday,
    required int totalTasksCompleted,
    required double totalXp,
    int sessionDurationMinutes = 0,
    bool streakAtRisk = false,
    bool justBrokeStreak = false,
    bool isNewUser = false,
    int daysSinceLastActivity = 0,
    bool firstEpiphany = false,
    int sourcesUsed = 0,
    bool milestoneReached = false,
    String? milestoneType,
  }) {
    final hour = DateTime.now().hour;
    TimeOfDay timeOfDay;
    
    if (hour >= 6 && hour < 12) {
      timeOfDay = TimeOfDay.morning;
    } else if (hour >= 12 && hour < 18) {
      timeOfDay = TimeOfDay.afternoon;
    } else if (hour >= 18 && hour < 24) {
      timeOfDay = TimeOfDay.evening;
    } else {
      timeOfDay = TimeOfDay.night;
    }

    return MotivationContext(
      timeOfDay: timeOfDay,
      sessionState: sessionState,
      streakDays: streakDays,
      tasksCompletedToday: tasksCompletedToday,
      totalTasksCompleted: totalTasksCompleted,
      totalXp: totalXp,
      sessionDurationMinutes: sessionDurationMinutes,
      streakAtRisk: streakAtRisk,
      justBrokeStreak: justBrokeStreak,
      isNewUser: isNewUser,
      daysSinceLastActivity: daysSinceLastActivity,
      firstEpiphany: firstEpiphany,
      sourcesUsed: sourcesUsed,
      milestoneReached: milestoneReached,
      milestoneType: milestoneType,
    );
  }
}
```

### 3.3 Motivation Engine

```dart
// lib/core/motivation/motivation_engine.dart

import 'dart:math';
import '../../data/motivation/models/motivation_text.dart';
import '../../data/motivation/models/motivation_context.dart';
import 'motivation_texts.dart';

class MotivationEngine {
  final Random _random = Random();
  final Map<String, DateTime> _recentlyShown = {};
  
  // Минимальное время между показами одного текста (в часах)
  static const int _minRepeatHours = 24;
  
  // Максимальное количество текстов в истории
  static const int _maxRecentHistory = 10;

  MotivationText? getTextForContext(MotivationContext context) {
    // Приоритетный порядок проверки условий
    final candidates = <MotivationText>[];
    
    // 1. Проверяем milestone достижения
    if (context.milestoneReached && context.milestoneType != null) {
      final milestoneTexts = _getTextsByCondition(context.milestoneType!);
      candidates.addAll(milestoneTexts);
    }
    
    // 2. Проверяем стрик
    if (context.streakAtRisk) {
      candidates.addAll(_getTextsByTrigger('streak_risk'));
    }
    if (context.justBrokeStreak) {
      candidates.addAll(_getTextsByTrigger('streak_broken'));
    }
    if (context.streakDays >= 100) {
      candidates.addAll(_getTextsByCondition('streak_100'));
    } else if (context.streakDays >= 30) {
      candidates.addAll(_getTextsByCondition('streak_30'));
    } else if (context.streakDays >= 7) {
      candidates.addAll(_getTextsByCondition('streak_7'));
    }
    
    // 3. Проверяем состояние сессии
    if (context.sessionState == SessionState.stuck) {
      candidates.addAll(_getTextsByTrigger('stuck_15min'));
    }
    if (context.sessionDurationMinutes >= 30) {
      candidates.addAll(_getTextsByTrigger('session_30min'));
    }
    if (context.sessionDurationMinutes >= 60) {
      candidates.addAll(_getTextsByTrigger('session_very_long'));
    }
    if (context.sessionState == SessionState.hintUsed) {
      candidates.addAll(_getTextsByTrigger('hint_requested'));
    }
    
    // 4. Если кандидатов нет, выбираем по времени суток
    if (candidates.isEmpty) {
      candidates.addAll(_getTextsForTimeOfDay(context.timeOfDay));
    }
    
    // Фильтруем недавно показанные
    final available = candidates.where((t) => !_wasRecentlyShown(t.id)).toList();
    
    if (available.isEmpty) {
      // Если все показаны недавно, берём любой с наименьшим count
      candidates.sort((a, b) => 
          (a.shownCount).compareTo(b.shownCount));
      return candidates.isNotEmpty ? candidates.first : null;
    }
    
    // Выбираем случайный из доступных
    return available[_random.nextInt(available.length)];
  }

  List<MotivationText> _getTextsByCondition(String condition) {
    return MotivationTexts.all
        .where((t) => t.condition == condition)
        .toList();
  }

  List<MotivationText> _getTextsByTrigger(String trigger) {
    return MotivationTexts.all
        .where((t) => t.trigger == trigger)
        .toList();
  }

  List<MotivationText> _getTextsForTimeOfDay(TimeOfDay timeOfDay) {
    List<MotivationCategory> preferredCategories;
    
    switch (timeOfDay) {
      case TimeOfDay.morning:
        // Утром — энергичные и про будущее
        preferredCategories = [
          MotivationCategory.energetic,
          MotivationCategory.career,
          MotivationCategory.thinking,
        ];
        break;
      case TimeOfDay.afternoon:
        // Днём — про практику и упорство
        preferredCategories = [
          MotivationCategory.practical,
          MotivationCategory.perseverance,
          MotivationCategory.thinking,
        ];
        break;
      case TimeOfDay.evening:
        // Вечером — про удовлетворение и цитаты
        preferredCategories = [
          MotivationCategory.satisfaction,
          MotivationCategory.quotes,
          MotivationCategory.thinking,
        ];
        break;
      case TimeOfDay.night:
        // Ночью — спокойные, про отдых
        preferredCategories = [
          MotivationCategory.session,
          MotivationCategory.quotes,
        ];
        break;
    }
    
    return MotivationTexts.all
        .where((t) => preferredCategories.contains(t.category))
        .toList();
  }

  bool _wasRecentlyShown(String id) {
    final lastShown = _recentlyShown[id];
    if (lastShown == null) return false;
    
    final hoursSinceShown = DateTime.now().difference(lastShown).inHours;
    return hoursSinceShown < _minRepeatHours;
  }

  void markAsShown(String id) {
    _recentlyShown[id] = DateTime.now();
    
    // Очищаем старые записи
    if (_recentlyShown.length > _maxRecentHistory) {
      final sortedKeys = _recentlyShown.keys.toList()
        ..sort((a, b) => _recentlyShown[a]!.compareTo(_recentlyShown[b]!));
      
      for (int i = 0; i < sortedKeys.length - _maxRecentHistory; i++) {
        _recentlyShown.remove(sortedKeys[i]);
      }
    }
  }

  // Специальные методы для конкретных ситуаций

  MotivationText? getOnboardingText() {
    final texts = MotivationTexts.all
        .where((t) => t.category == MotivationCategory.thinking)
        .toList();
    return texts.isNotEmpty ? texts[_random.nextInt(texts.length)] : null;
  }

  MotivationText? getSessionStartText({bool isDifficult = false}) {
    if (isDifficult) {
      final texts = MotivationTexts.all
          .where((t) => t.category == MotivationCategory.perseverance)
          .toList();
      return texts.isNotEmpty ? texts[_random.nextInt(texts.length)] : null;
    }
    
    final texts = MotivationTexts.all
        .where((t) => 
            t.category == MotivationCategory.energetic ||
            t.category == MotivationCategory.thinking)
        .toList();
    return texts.isNotEmpty ? texts[_random.nextInt(texts.length)] : null;
  }

  MotivationText? getCompletionText({int difficulty = 3}) {
    late MotivationCategory category;
    
    if (difficulty >= 4) {
      category = MotivationCategory.satisfaction;
    } else {
      category = MotivationCategory.energetic;
    }
    
    final texts = MotivationTexts.all
        .where((t) => t.category == category)
        .toList();
    return texts.isNotEmpty ? texts[_random.nextInt(texts.length)] : null;
  }

  MotivationText? getStreakText(int days, {bool atRisk = false}) {
    if (atRisk) {
      return _getTextsByTrigger('streak_risk').firstOrNull;
    }
    
    if (days >= 100) {
      return _getTextsByCondition('streak_100').firstOrNull;
    } else if (days >= 30) {
      return _getTextsByCondition('streak_30').firstOrNull;
    } else if (days >= 7) {
      return _getTextsByCondition('streak_7').firstOrNull;
    }
    
    // Общий текст для активного стрика
    final text = _getTextsByTrigger('streak_active').firstOrNull;
    if (text != null) {
      return MotivationText(
        id: text.id,
        text: text.text.replaceAll('{days}', days.toString()),
        author: text.author,
        tags: text.tags,
        category: text.category,
      );
    }
    
    return null;
  }
}
```

---

## 4. UI Компоненты

### 4.1 Motivation Card

```dart
// lib/presentation/widgets/motivation/motivation_card.dart

import 'package:flutter/material.dart';
import '../../../data/motivation/models/motivation_text.dart';

class MotivationCard extends StatelessWidget {
  final MotivationText motivation;
  final VoidCallback? onDismiss;
  final bool showAuthor;
  final bool animate;

  const MotivationCard({
    super.key,
    required this.motivation,
    this.onDismiss,
    this.showAuthor = true,
    this.animate = true,
  });

  @override
  Widget build(BuildContext context) {
    final widget = Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Theme.of(context).colorScheme.primaryContainer,
            Theme.of(context).colorScheme.secondaryContainer,
          ],
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Theme.of(context).colorScheme.shadow.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          // Icon
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.primary.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(
                  _getCategoryIcon(motivation.category),
                  size: 20,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
              const SizedBox(width: 12),
              Text(
                _getCategoryTitle(motivation.category),
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
          
          const SizedBox(height: 16),
          
          // Text
          Text(
            motivation.text,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              fontSize: 16,
              height: 1.5,
            ),
          ),
          
          // Author
          if (showAuthor && motivation.author != null) ...[
            const SizedBox(height: 12),
            Text(
              '— ${motivation.author}',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                fontStyle: FontStyle.italic,
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
          ],
          
          // Dismiss button
          if (onDismiss != null) ...[
            const SizedBox(height: 12),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: onDismiss,
                child: const Text('Понятно'),
              ),
            ),
          ],
        ],
      ),
    );

    if (animate) {
      return TweenAnimationBuilder<double>(
        tween: Tween(begin: 0, end: 1),
        duration: const Duration(milliseconds: 500),
        curve: Curves.easeOutCubic,
        builder: (context, value, child) {
          return Transform.translate(
            offset: Offset(0, 20 * (1 - value)),
            child: Opacity(
              opacity: value,
              child: child,
            ),
          );
        },
        child: widget,
      );
    }

    return widget;
  }

  IconData _getCategoryIcon(MotivationCategory category) {
    switch (category) {
      case MotivationCategory.thinking:
        return Icons.psychology;
      case MotivationCategory.practical:
        return Icons.build;
      case MotivationCategory.satisfaction:
        return Icons.emoji_events;
      case MotivationCategory.career:
        return Icons.trending_up;
      case MotivationCategory.perseverance:
        return Icons.fitness_center;
      case MotivationCategory.energetic:
        return Icons.bolt;
      case MotivationCategory.quotes:
        return Icons.format_quote;
      case MotivationCategory.session:
        return Icons.timer;
      case MotivationCategory.streak:
        return Icons.local_fire_department;
      case MotivationCategory.achievements:
        return Icons.star;
    }
  }

  String _getCategoryTitle(MotivationCategory category) {
    switch (category) {
      case MotivationCategory.thinking:
        return 'Развитие мышления';
      case MotivationCategory.practical:
        return 'Практическая польза';
      case MotivationCategory.satisfaction:
        return 'Удовлетворение';
      case MotivationCategory.career:
        return 'Будущее и карьера';
      case MotivationCategory.perseverance:
        return 'Преодоление';
      case MotivationCategory.energetic:
        return 'Мотивация';
      case MotivationCategory.quotes:
        return 'Цитата';
      case MotivationCategory.session:
        return 'Совет';
      case MotivationCategory.streak:
        return 'Стрик';
      case MotivationCategory.achievements:
        return 'Достижение';
    }
  }
}
```

### 4.2 Motivation Banner

```dart
// lib/presentation/widgets/motivation/motivation_banner.dart

import 'package:flutter/material.dart';
import '../../../data/motivation/models/motivation_text.dart';

class MotivationBanner extends StatelessWidget {
  final MotivationText motivation;
  final VoidCallback? onTap;
  final VoidCallback? onDismiss;

  const MotivationBanner({
    super.key,
    required this.motivation,
    this.onTap,
    this.onDismiss,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      onHorizontalDragEnd: onDismiss != null
          ? (_) => onDismiss!()
          : null,
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceVariant,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: Theme.of(context).colorScheme.outlineVariant,
          ),
        ),
        child: Row(
          children: [
            Icon(
              Icons.lightbulb_outline,
              color: Theme.of(context).colorScheme.primary,
              size: 20,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                motivation.text,
                style: Theme.of(context).textTheme.bodyMedium,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            if (onDismiss != null) ...[
              const SizedBox(width: 8),
              GestureDetector(
                onTap: onDismiss,
                child: Icon(
                  Icons.close,
                  size: 18,
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

### 4.3 Motivation Popup

```dart
// lib/presentation/widgets/motivation/motivation_popup.dart

import 'package:flutter/material.dart';
import '../../../data/motivation/models/motivation_text.dart';
import 'motivation_card.dart';

class MotivationPopup {
  static Future<void> show({
    required BuildContext context,
    required MotivationText motivation,
    bool barrierDismissible = true,
  }) async {
    return showDialog(
      context: context,
      barrierDismissible: barrierDismissible,
      barrierColor: Colors.black54,
      builder: (context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: MotivationCard(
            motivation: motivation,
            onDismiss: () => Navigator.pop(context),
          ),
        ),
      ),
    );
  }

  static Future<void> showAchievement({
    required BuildContext context,
    required MotivationText motivation,
  }) async {
    return showGeneralDialog(
      context: context,
      barrierDismissible: true,
      barrierColor: Colors.transparent,
      transitionDuration: const Duration(milliseconds: 400),
      pageBuilder: (context, animation, secondaryAnimation) {
        return Center(
          child: Container(
            margin: const EdgeInsets.all(24),
            child: ScaleTransition(
              scale: CurvedAnimation(
                parent: animation,
                curve: Curves.elasticOut,
              ),
              child: MotivationCard(
                motivation: motivation,
                animate: false,
                showAuthor: false,
                onDismiss: () => Navigator.pop(context),
              ),
            ),
          ),
        );
      },
    );
  }
}
```

---

## 5. Интеграция с Riverpod

### 5.1 Provider

```dart
// lib/presentation/providers/motivation_provider.dart

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/motivation/motivation_engine.dart';
import '../../data/motivation/models/motivation_text.dart';
import '../../data/motivation/models/motivation_context.dart';
import '../providers/gamification_provider.dart';

final motivationEngineProvider = Provider<MotivationEngine>((ref) {
  return MotivationEngine();
});

final motivationProvider = Provider<MotivationText?>((ref) {
  final engine = ref.watch(motivationEngineProvider);
  final gamification = ref.watch(gamificationMeProvider);
  
  // Строим контекст
  final context = MotivationContext.current(
    sessionState: SessionState.idle,
    streakDays: gamification?.streakCurrent ?? 0,
    tasksCompletedToday: gamification?.solvedTasksToday ?? 0,
    totalTasksCompleted: 0, // TODO: from stats
    totalXp: gamification?.totalXp ?? 0,
  );
  
  final text = engine.getTextForContext(context);
  
  if (text != null) {
    engine.markAsShown(text.id);
  }
  
  return text;
});

// Провайдеры для конкретных ситуаций

final sessionStartMotivationProvider = Provider.family<MotivationText?, bool>(
  (ref, isDifficult) {
    final engine = ref.watch(motivationEngineProvider);
    return engine.getSessionStartText(isDifficult: isDifficult);
  },
);

final completionMotivationProvider = Provider.family<MotivationText?, int>(
  (ref, difficulty) {
    final engine = ref.watch(motivationEngineProvider);
    return engine.getCompletionText(difficulty: difficulty);
  },
);

final streakMotivationProvider = Provider.family<MotivationText?, ({int days, bool atRisk})>(
  (ref, params) {
    final engine = ref.watch(motivationEngineProvider);
    return engine.getStreakText(params.days, atRisk: params.atRisk);
  },
);
```

### 5.2 Использование в экранах

```dart
// Пример использования в HomeScreen

class HomeScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final motivation = ref.watch(motivationProvider);
    
    return Scaffold(
      body: Column(
        children: [
          // ... other widgets
          
          if (motivation != null)
            Padding(
              padding: const EdgeInsets.all(16),
              child: MotivationBanner(
                motivation: motivation,
                onDismiss: () {
                  // Refresh provider to get new motivation
                  ref.invalidate(motivationProvider);
                },
              ),
            ),
          
          // ... rest of UI
        ],
      ),
    );
  }
}
```

---

## 6. AI-генерация персонализированных текстов (Future)

### 6.1 Концепция

В будущем модуль может генерировать персонализированные мотивационные тексты с помощью AI:

```dart
// lib/core/motivation/ai_motivation_generator.dart

class AiMotivationGenerator {
  final String apiKey;
  
  Future<MotivationText> generatePersonalized({
    required MotivationContext context,
    required String personaId,
  }) async {
    final prompt = _buildPrompt(context);
    
    // Call AI API
    final response = await _callAi(prompt, personaId);
    
    return MotivationText(
      id: 'ai_${DateTime.now().millisecondsSinceEpoch}',
      text: response,
      category: _determineCategory(context),
      tags: ['ai_generated', 'personalized'],
    );
  }
  
  String _buildPrompt(MotivationContext context) {
    return '''
Сгенерируй короткий (1-2 предложения) мотивирующий текст для студента, который:
- Решает задачи уже ${context.sessionDurationMinutes} минут
- Имеет стрик ${context.streakDays} дней
- Решил сегодня ${context.tasksCompletedToday} задач
- ${context.streakAtRisk ? "Рискует потерять стрик сегодня" : ""}

Текст должен быть вдохновляющим, но не пафосным.
''';
  }
}
```

---

## 7. Аналитика

### 7.1 Отслеживание показов

```dart
// Рекомендуется отслеживать:
- Как часто показываются тексты разных категорий
- Какие тексты чаще dismissed
- Влияют ли тексты на retention
- Корреляция между показом и продолжением сессии
```

---

## 8. Резюме

| Компонент | Назначение |
|-----------|------------|
| `MotivationText` | Модель текста с метаданными |
| `MotivationContext` | Контекст пользователя для выбора текста |
| `MotivationEngine` | Логика выбора подходящего текста |
| `MotivationCard` | Карточка для popup/dialog |
| `MotivationBanner` | Баннер в HomeScreen |
| `MotivationPopup` | Popup для достижений |

### Категории текстов: 10

| Категория | Количество текстов | Когда показывается |
|-----------|-------------------|-------------------|
| thinking | 6+ | Утро/день, общее развитие |
| practical | 5+ | День, практика |
| satisfaction | 4+ | Вечер, после решения |
| career | 4+ | Утро, мотивация |
| perseverance | 6+ | Сложные задачи |
| energetic | 5+ | Начало сессии |
| quotes | 7+ | Вечер/ночь |
| session | 5+ | Во время сессии |
| streak | 6+ | Стрик события |
| achievements | 7+ | Достижения |

---

*Документация модуля мотивации для Flutter приложения "Лежандр"*
