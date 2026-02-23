from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum, JSON, Date, Index, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, date
import enum

Base = declarative_base()


class VoteTargetType(enum.Enum):
    """Типы сущностей, за которые можно голосовать"""
    problem = "problem"
    solution = "solution"
    article = "article"
    comment = "comment"


class ArticleType(enum.Enum):
    """Типы статей"""
    problem_explainer = "problem_explainer"  # Разбор задачи
    motivational = "motivational"  # Мотивирующая статья
    weekly_digest = "weekly_digest"  # Еженедельный отчёт
    epiphanies_collection = "epiphanies_collection"  # Подборка озарений


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


class UserRole(str, enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"

class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    device_id = Column(String, unique=True, index=True, nullable=True)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    role = Column(String, default=UserRole.user, nullable=False, index=True)
    
    # Связи
    solutions = relationship("UserSolution", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    articles = relationship("Article", back_populates="author")
    votes = relationship("Vote", back_populates="user")
    gamification = relationship("UserGamification", back_populates="user", uselist=False)
    xp_events = relationship("XpEvent", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    reference = Column(String)
    condition_text = Column(Text)
    condition_img = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # Связь с решениями
    source_obj = relationship("Source", back_populates="problems")
    tags = relationship("Tag", secondary="problem_tags", back_populates="problems")
    solutions = relationship("UserSolution", back_populates="problem")
    comments = relationship("Comment", back_populates="problem")
    concepts = relationship("ProblemConcept", back_populates="problem")

class UserSolution(Base):
    __tablename__ = "user_solutions"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    status = Column(String, default="active")
    personal_difficulty = Column(Integer, nullable=True)
    quality_score = Column(Float, nullable=True)
    xp_earned = Column(Float, default=0)
    user_notes = Column(Text, nullable=True)
    solution_img_path = Column(String, nullable=True)
    solution_text = Column(Text, nullable=True)  # Текстовое описание решения (Markdown с LaTeX), сгенерированное из изображения
    total_minutes = Column(Float, default=0)

    problem = relationship("Problem", back_populates="solutions")
    user = relationship("User", back_populates="solutions")
    sessions = relationship("Session", back_populates="solution")
    epiphanies = relationship("Epiphany", back_populates="solution")
    questions = relationship("Question", back_populates="solution")
    hints = relationship("Hint", back_populates="solution")
    comments = relationship("Comment", back_populates="solution")
    articles = relationship("Article", back_populates="solution")
    concepts = relationship("SolutionConcept", back_populates="solution")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("user_solutions.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Float)

    solution = relationship("UserSolution", back_populates="sessions")

class Epiphany(Base):
    __tablename__ = "epiphanies"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("user_solutions.id"))
    # Описание озарения (текст/LaTeX)
    description = Column(Text, nullable=False)
    # Визуализация (опционально)
    image_path = Column(String, nullable=True)
    # Сила озарения: 1 (маленькая догадка), 2 (важный ход), 3 (game changer)
    magnitude = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    # Связь с решением
    solution = relationship("UserSolution", back_populates="epiphanies")


class Question(Base):
    """Модель вопроса, возникшего в ходе решения задачи"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("user_solutions.id"), nullable=False, index=True)
    # Текст вопроса
    body = Column(Text, nullable=False)
    # Контекст вопроса (опционально - фото черновика, где возник вопрос)
    image_path = Column(String, nullable=True)
    # Ответ на вопрос (может быть заполнен позже пользователем или AI)
    answer = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Связь с решением
    solution = relationship("UserSolution", back_populates="questions")


class Hint(Base):
    """Модель совета от AI по решению задачи"""
    __tablename__ = "hints"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("user_solutions.id"), nullable=False, index=True)
    
    # Текст совета от AI (Nullable, т.к. создается Draft)
    hint_text = Column(Text, nullable=True)
    
    # Статус генерации: pending -> processing -> completed / failed
    status = Column(String, default="pending")
    
    # Заметки пользователя к конкретной просьбе подсказки
    user_notes = Column(Text, nullable=True)

    # Модель AI, которая дала совет
    ai_model = Column(String, nullable=True)
    # Промпт, использованный для генерации совета
    prompt_used = Column(Text, nullable=True)
    # Контекст (фото черновика, которое было отправлено в AI)
    context_image_path = Column(String, nullable=True)
    # Влияет ли использование совета на XP (штраф за подсказку)
    xp_penalty = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    
    # Связь с решением
    solution = relationship("UserSolution", back_populates="hints")


class Comment(Base):
    """Модель комментария"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=True, index=True)
    solution_id = Column(Integer, ForeignKey("user_solutions.id"), nullable=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True, index=True)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True, index=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False)
    is_approved = Column(Boolean, nullable=True)  # NULL = не проверен, True/False = результат модерации

    # Связи
    user = relationship("User", back_populates="comments")
    problem = relationship("Problem")
    solution = relationship("UserSolution", back_populates="comments")
    article = relationship("Article", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")


class Article(Base):
    """Модель статьи/поста"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=True)
    solution_id = Column(Integer, ForeignKey("user_solutions.id"), nullable=True)
    # Тип статьи
    article_type = Column(SQLEnum(ArticleType), nullable=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_published = Column(Boolean, default=False)
    meta = Column(JSON, nullable=True)  # Метаданные (модель LLM, промпт и т.п.)

    # Связи
    author = relationship("User", back_populates="articles")
    problem = relationship("Problem")
    solution = relationship("UserSolution", back_populates="articles")
    comments = relationship("Comment", back_populates="article")


class Vote(Base):
    """Модель голоса/лайка"""
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_type = Column(SQLEnum(VoteTargetType), nullable=False, index=True)
    target_id = Column(Integer, nullable=False, index=True)
    value = Column(Integer, default=1)  # +1 (лайк) или -1 (дизлайк)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="votes")

    # Явное указание индекса, чтобы Alembic не пытался его пересоздавать/удалять
    __table_args__ = (
        Index('ix_votes_user_target_unique', 'user_id', 'target_type', 'target_id', unique=True),
    )

class UserGamification(Base):
    """Модель геймификационного состояния пользователя"""
    __tablename__ = "user_gamification"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    total_xp = Column(Float, default=0.0)
    current_hearts = Column(Integer, default=5)
    max_hearts = Column(Integer, default=5)
    streak_current = Column(Integer, default=0)
    streak_best = Column(Integer, default=0)
    last_activity_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Связи
    user = relationship("User", back_populates="gamification")
    
    # Явное указание уникального индекса, созданного в миграции c3d4e5f6a7b8
    # оно будет отвечать за поиск
    __table_args__ = (
        Index('ix_user_gamification_user_id', 'user_id', unique=True),
    )

class XpEvent(Base):
    """Модель события изменения XP"""
    __tablename__ = "xp_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    solution_id = Column(Integer, ForeignKey("user_solutions.id"), nullable=True, index=True)
    event_type = Column(SQLEnum(XpEventType), nullable=False, index=True)
    delta_xp = Column(Float, nullable=False)
    meta = Column(JSON, nullable=True)  # Дополнительные данные (сложность, качество, величина озарения, ID подсказки и т.п.)
    created_at = Column(DateTime, default=datetime.now, index=True)

    # Связи
    user = relationship("User", back_populates="xp_events")
    solution = relationship("UserSolution")

# Финансовые таблицы

class TransactionType(enum.Enum):
    deposit = "deposit"          # Пополнение
    spend = "spend"              # Списание
    refund = "refund"            # Возврат
    manual = "manual"            # Ручная корректировка

class UserBalance(Base):
    __tablename__ = "user_balances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    
    # Лимиты для Free-tier (Кот Базис)
    daily_free_uses = Column(Integer, default=0)
    last_free_use_date = Column(Date, default=datetime.now().date)
    
    user = relationship("User", backref="balance_obj")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    status = Column(String, default="pending")  # pending, succeeded, canceled
    
    description = Column(String, nullable=True)
    payment_id = Column(String, nullable=True, index=True) # ID счета в YooKassa (invoice_id)
    payment_url = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="transactions")


# --- КОНЦЕПТЫ И ГРАФ ЗНАНИЙ (НОВОЕ) ---

# Таблица зависимостей (Граф: Что нужно знать ДО)
# Parent -> Child (чтобы понять Child, нужно знать Parent)
concept_dependencies = Table(
    "concept_dependencies",
    Base.metadata,
    Column("parent_id", Integer, ForeignKey("concepts.id"), primary_key=True),
    Column("child_id", Integer, ForeignKey("concepts.id"), primary_key=True)
)

class Concept(Base):
    """
    Атомарная единица знания / Навык.
    Может быть 'Канонической' (основной) или 'Алиасом' (ссылкой на другую).
    """
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False) # Не unique, т.к. могут быть дубли до склейки
    slug = Column(String, unique=True, index=True, nullable=False)
    
    # Описательная часть
    description = Column(Text, nullable=True)         # Теория / Определение
    utility_description = Column(Text, nullable=True) # "Зачем это нужно?" (Практическая польза)

    # Механизм борьбы с дубликатами (Aliasing)
    # Если alias_of_id заполнено, значит этот концепт - просто синоним другого.
    alias_of_id = Column(Integer, ForeignKey("concepts.id"), nullable=True, index=True)
    
    # Модерация
    is_public = Column(Boolean, default=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    moderation_status = Column(String, default="pending") # pending, approved, merged, rejected
    moderation_reason = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now)

    # Связи
    # Алиас знает, на кого он ссылается
    canonical_concept = relationship("Concept", remote_side=[id], backref="aliases")

    # Связи с задачами и решениями
    problems = relationship("ProblemConcept", back_populates="concept")
    solutions = relationship("SolutionConcept", back_populates="concept")
    
    # Граф зависимостей (Many-to-Many self-referential)
    parents = relationship(
        "Concept",
        secondary=concept_dependencies,
        primaryjoin=id==concept_dependencies.c.child_id,
        secondaryjoin=id==concept_dependencies.c.parent_id,
        backref="children"
    )

class ProblemConcept(Base):
    """
    Knowledge Map: Какие знания заложены в условие задачи.
    """
    __tablename__ = "problem_concepts"

    problem_id = Column(Integer, ForeignKey("problems.id"), primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), primary_key=True)
    
    # AI объясняет, где именно в задаче спрятан этот концепт
    explanation = Column(Text, nullable=True) 
    # Вес (1.0 - основная тема, 0.1 - косвенно упоминается)
    relevance = Column(Float, default=1.0)

    problem = relationship("Problem", back_populates="concepts")
    concept = relationship("Concept", back_populates="problems")

class SolutionConcept(Base):
    """
    Trace: Какие методы/концепты применил пользователь в решении.
    """
    __tablename__ = "solution_concepts"

    solution_id = Column(Integer, ForeignKey("user_solutions.id"), primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), primary_key=True)
    
    # AI цитирует часть решения или описывает контекст применения
    # Например: "Использовано в строке 3 для упрощения дроби"
    usage_context = Column(Text, nullable=True) 

    solution = relationship("UserSolution", back_populates="concepts")
    concept = relationship("Concept", back_populates="solutions")