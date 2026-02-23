#!/usr/bin/env python3
"""
Mental Math Trainer - CLI Client
Контекст: конфигурация, хранение токена, UI утилиты
"""
import os
import json
import secrets
from pathlib import Path
from datetime import datetime

# --- КОНФИГУРАЦИЯ ---
API_URL = "http://localhost:8000/api/v1"
TOKEN_FILE = Path(".mm_token")
ACCOUNT_KEY_FILE = Path(".mm_account")


class Context:
    """Системный контекст: управление файлами и выводом."""
    
    @staticmethod
    def load_token() -> str | None:
        """Загрузить токен из файла."""
        if TOKEN_FILE.exists():
            return TOKEN_FILE.read_text().strip()
        return None

    @staticmethod
    def save_token(token: str):
        """Сохранить токен в файл."""
        TOKEN_FILE.write_text(token)

    @staticmethod
    def load_account_key() -> str | None:
        """Загрузить account_key из файла."""
        if ACCOUNT_KEY_FILE.exists():
            return ACCOUNT_KEY_FILE.read_text().strip()
        return None

    @staticmethod
    def save_account_key(key: str):
        """Сохранить account_key в файл."""
        ACCOUNT_KEY_FILE.write_text(key)

    @staticmethod
    def get_or_create_account_key() -> str:
        """Получить или создать account_key."""
        key = Context.load_account_key()
        if key:
            return key
        key = secrets.token_urlsafe(32)
        Context.save_account_key(key)
        return key

    # --- UI HELPERS ---
    
    @staticmethod
    def print_header(text: str):
        print(f"\n{'='*50}")
        print(f"  {text}")
        print('='*50)

    @staticmethod
    def print_success(text: str):
        print(f"✅ {text}")

    @staticmethod
    def print_error(text: str):
        print(f"❌ {text}")

    @staticmethod
    def print_info(text: str):
        print(f"ℹ️  {text}")
        
    @staticmethod
    def print_task(text: str):
        print(f"📝 {text}")
        
    @staticmethod
    def print_xp(xp: int):
        print(f"⭐ +{xp} XP")

    @staticmethod
    def input_default(prompt: str, default: str) -> str:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default
    
    @staticmethod
    def input_int(prompt: str, default: int = 0) -> int:
        val = input(f"{prompt} [{default}]: ").strip()
        try:
            return int(val) if val else default
        except ValueError:
            return default
    
    @staticmethod
    def input_float(prompt: str, default: float = 0.0) -> float:
        val = input(f"{prompt} [{default}]: ").strip()
        try:
            return float(val.replace(",", ".")) if val else default
        except ValueError:
            return default
    
    @staticmethod
    def draw_bar(value: float, max_val: float, width: int = 20) -> str:
        """Рисует ASCII бар прогресса."""
        if max_val <= 0:
            return ""
        ratio = min(value / max_val, 1.0)
        bar_len = int(ratio * width)
        return "█" * bar_len + "░" * (width - bar_len)
    
    @staticmethod
    def format_time(seconds: int) -> str:
        """Форматирует время в MM:SS."""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"
    
    @staticmethod
    def format_expression(expr: str) -> str:
        """Форматирует LaTeX выражение для вывода."""
        # Простая замена для терминала
        return expr.replace("\\times", "×").replace("\\div", "÷").replace("\\cdot", "·")
    
    @staticmethod
    def clear_screen():
        """Очистить экран."""
        os.system('clear' if os.name == 'posix' else 'cls')
