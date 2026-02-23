#!/usr/bin/env python3
"""
Mental Math Trainer - API Client
"""
import requests
from mm_context import Context, API_URL


class MentalMathAPI:
    """API клиент для Mental Math Trainer."""
    
    def __init__(self):
        self.token = Context.load_token()
        self.user = None
        self.progress = None

    @property
    def headers(self) -> dict:
        """Заголовки с авторизацией."""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response | None:
        """Базовый метод запроса."""
        url = f"{API_URL}/{endpoint}"
        req_headers = self.headers.copy()
        if 'headers' in kwargs:
            req_headers.update(kwargs['headers'])
            del kwargs['headers']
        
        try:
            resp = requests.request(method, url, headers=req_headers, **kwargs)
        except requests.exceptions.ConnectionError:
            Context.print_error("Нет соединения с сервером. Запущен ли сервер?")
            return None
        except Exception as e:
            Context.print_error(f"Ошибка сети: {e}")
            return None

        # Обработка 401 - токен истек
        if resp.status_code == 401:
            Context.print_info("Токен истек. Перерегистрация...")
            if self.register():
                req_headers = self.headers.copy()
                try:
                    resp = requests.request(method, url, headers=req_headers, **kwargs)
                except Exception as e:
                    Context.print_error(f"Ошибка при повторе: {e}")
                    return None
            else:
                Context.print_error("Не удалось обновить сессию.")
                return None
        
        return resp

    # --- AUTH ---
    
    def register(self) -> bool:
        """Регистрация/вход по account_key."""
        account_key = Context.get_or_create_account_key()
        try:
            resp = requests.post(
                f"{API_URL}/auth/register",
                json={"account_key": account_key}
            )
            if resp.status_code == 200:
                data = resp.json()
                self.token = data["access_token"]
                Context.save_token(self.token)
                return True
        except Exception:
            pass
        return False

    def login(self, account_key: str) -> bool:
        """Вход по account_key."""
        try:
            resp = requests.post(
                f"{API_URL}/auth/login",
                json={"account_key": account_key}
            )
            if resp.status_code == 200:
                data = resp.json()
                self.token = data["access_token"]
                Context.save_token(self.token)
                Context.save_account_key(account_key)
                return True
        except Exception:
            pass
        return False

    def get_me(self) -> dict | None:
        """Получить информацию о пользователе."""
        resp = self._request("GET", "auth/me")
        if resp and resp.status_code == 200:
            self.user = resp.json()
            return self.user
        return None

    # --- PROGRESS ---
    
    def get_progress(self) -> dict | None:
        """Получить прогресс пользователя."""
        resp = self._request("GET", "progress/")
        if resp and resp.status_code == 200:
            self.progress = resp.json()
            return self.progress
        return None

    # --- LEVELS ---
    
    def get_levels(self) -> list:
        """Получить список уровней."""
        resp = self._request("GET", "tasks/levels")
        if resp and resp.status_code == 200:
            return resp.json().get("levels", [])
        return []

    def get_topics(self, level: int = None) -> list:
        """Получить список тем."""
        params = {"level": level} if level else {}
        resp = self._request("GET", "tasks/topics", params=params)
        if resp and resp.status_code == 200:
            return resp.json().get("topics", [])
        return []

    # --- TASKS ---
    
    def generate_task(self, level: int, sub_level: int = None, topic: str = None) -> dict | None:
        """Сгенерировать задачу."""
        payload = {"level": level}
        if sub_level:
            payload["sub_level"] = sub_level
        if topic:
            payload["topic"] = topic
        
        resp = self._request("POST", "tasks/generate", json=payload)
        if resp and resp.status_code == 200:
            return resp.json()
        return None

    def validate_answer(self, task_id: int, user_answer: str, 
                        mental_steps: int = 0, written_steps: int = 0,
                        time_seconds: int = 0, hints_used: int = 0) -> dict | None:
        """Проверить ответ."""
        payload = {
            "task_id": task_id,
            "user_answer": user_answer,
            "mental_steps": mental_steps,
            "written_steps": written_steps,
            "time_seconds": time_seconds,
            "hints_used": hints_used
        }
        resp = self._request("POST", "tasks/validate", json=payload)
        if resp and resp.status_code == 200:
            return resp.json()
        return None

    def get_task(self, task_id: int) -> dict | None:
        """Получить задачу по ID."""
        resp = self._request("GET", f"tasks/{task_id}")
        if resp and resp.status_code == 200:
            return resp.json()
        return None

    def list_tasks(self, level: int = None, topic: str = None, 
                   limit: int = 20, offset: int = 0) -> list:
        """Получить список задач."""
        params = {"limit": limit, "offset": offset}
        if level:
            params["level"] = level
        if topic:
            params["topic"] = topic
        
        resp = self._request("GET", "tasks/", params=params)
        if resp and resp.status_code == 200:
            return resp.json()
        return []

    # --- SESSIONS ---
    
    def get_sessions(self, limit: int = 20, offset: int = 0) -> list:
        """Получить историю сессий."""
        resp = self._request("GET", "sessions/", params={"limit": limit, "offset": offset})
        if resp and resp.status_code == 200:
            return resp.json()
        return []

    def get_stats(self, days: int = 7) -> dict | None:
        """Получить статистику."""
        resp = self._request("GET", "sessions/stats", params={"days": days})
        if resp and resp.status_code == 200:
            return resp.json()
        return None
