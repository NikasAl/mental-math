import os
import requests
from mv_context import Context, API_URL

class BaseApiMixin:
    """Базовая логика запросов и авторизации"""
    def __init__(self):
        self.token = Context.load_token()
        self.user = None

    @property
    def headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def _request(self, method, endpoint, **kwargs):
        url = f"{API_URL}/{endpoint}"
        req_headers = self.headers.copy()
        if 'headers' in kwargs:
            req_headers.update(kwargs['headers'])
            del kwargs['headers']

        files = kwargs.get('files')
        file_positions = []
        if files:
            for key, value in files.items():
                if isinstance(value, tuple) and len(value) > 1 and hasattr(value[1], 'tell'):
                     file_positions.append((value[1], value[1].tell()))

        try:
            resp = requests.request(method, url, headers=req_headers, **kwargs)
        except Exception as e:
            Context.print_error(f"Ошибка сети: {e}")
            return None

        if resp.status_code == 401:
            Context.print_info("Токен истек. Обновление сессии...")
            if self.device_login():
                req_headers = self.headers.copy()
                for f_obj, pos in file_positions:
                    f_obj.seek(pos)
                try:
                    resp = requests.request(method, url, headers=req_headers, **kwargs)
                except Exception as e:
                    Context.print_error(f"Ошибка сети при повторе: {e}")
                    return None
            else:
                Context.print_error("Не удалось обновить сессию. Требуется перезапуск.")
        
        return resp

    def device_login(self):
        device_id, secret = Context.get_or_create_device_creds()
        payload = {"device_id": device_id, "secret_key": secret}
        try:
            resp = requests.post(f"{API_URL}/auth/device-register", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                self.token = data["access_token"]
                Context.save_token(self.token)
                return True
        except Exception:
            pass
        return False

    def login(self, email, password):
        try:
            resp = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
            if resp.status_code == 200:
                data = resp.json()
                self.token = data["access_token"]
                Context.save_token(self.token)
                return True
        except Exception:
            pass
        return False

    def get_me(self):
        resp = self._request("GET", "users/me")
        if resp and resp.status_code == 200:
            self.user = resp.json()
            return self.user
        return None
        
    def link_email(self, email, password, username=None):
        payload = {"email": email, "password": password, "username": username}
        resp = self._request("PATCH", "users/me/convert", json=payload)
        return resp.json() if resp and resp.status_code == 200 else None

class ProblemsApiMixin:
    def get_sources(self):
        resp = self._request("GET", "sources")
        return resp.json() if resp and resp.status_code == 200 else []

    def get_problem(self, problem_id):
        resp = self._request("GET", f"problems/{problem_id}")
        return resp.json() if resp and resp.status_code == 200 else None

    def update_problem_text(self, problem_id, text):
        payload = {"condition_text": text}
        resp = self._request("PATCH", f"problems/{problem_id}", json=payload)
        return resp.status_code == 200

    def get_problems(self, search=None, source=None):
        params = {}
        if search: params['search'] = search
        if source: params['source'] = source
        resp = self._request("GET", "problems", params=params)
        return resp.json() if resp and resp.status_code == 200 else []

    def create_problem(self, reference, source_name, tags, condition_text):
        payload = {
            "reference": reference,
            "source_name": source_name,
            "tags": tags,
            "condition_text": condition_text
        }
        resp = self._request("POST", "problems", json=payload)
        return resp.json() if resp and resp.status_code == 201 else None

    def get_tags(self, search=None):
        params = {"search": search} if search else {}
        resp = self._request("GET", "tags", params=params)
        return resp.json() if resp and resp.status_code == 200 else []

    def merge_tags(self, target_id, source_ids):
        payload = {"target_tag_id": target_id, "source_tag_ids": source_ids}
        resp = self._request("POST", "tags/merge", json=payload)
        return resp.json() if resp and resp.status_code == 200 else None

class SolutionsApiMixin:
    def get_active_solutions(self):
        resp = self._request("GET", "solutions", params={"status": "active"})
        return resp.json() if resp and resp.status_code == 200 else []

    def get_solution(self, solution_id):
        resp = self._request("GET", f"solutions/{solution_id}")
        return resp.json() if resp and resp.status_code == 200 else None

    def update_solution_text(self, solution_id, text):
        payload = {"solution_text": text}
        resp = self._request("PATCH", f"solutions/{solution_id}", json=payload)
        return resp.status_code == 200

    def get_solutions(self, problem_id=None, status=None):
        params = {}
        if problem_id: params['problem_id'] = problem_id
        if status: params['status'] = status
        resp = self._request("GET", "solutions", params=params)
        return resp.json() if resp and resp.status_code == 200 else []

    def create_solution(self, problem_id):
        resp = self._request("POST", "solutions", json={"problem_id": problem_id})
        return resp.json() if resp and resp.status_code in [200, 201] else None

    def finish_solution(self, solution_id, status, difficulty, quality, notes):
        payload = {
            "status": status,
            "personal_difficulty": difficulty,
            "quality_score": quality,
            "user_notes": notes
        }
        resp = self._request("PATCH", f"solutions/{solution_id}", json=payload)
        return resp.json() if resp and resp.status_code == 200 else None
        
    def post_session(self, solution_id, start, end, duration):
        payload = {
            "solution_id": solution_id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "duration": duration
        }
        resp = self._request("POST", "sessions", json=payload)
        return resp and resp.status_code == 201

class ArtifactsApiMixin:
    def upload_image(self, category, entity_id, file_path):
        if not file_path or not os.path.exists(file_path):
            return False
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "image/png")}
            resp = self._request("POST", f"uploads/{category}/{entity_id}", files=files)
        if resp and resp.status_code != 200:
             Context.print_error(f"Ошибка загрузки: {resp.text}")
        return resp and resp.status_code == 200

    def create_epiphany(self, solution_id, description, magnitude):
        payload = {"solution_id": solution_id, "description": description, "magnitude": magnitude}
        resp = self._request("POST", "epiphanies", json=payload)
        return resp.json() if resp and resp.status_code == 201 else None

    def get_questions(self, solution_id):
        resp = self._request("GET", f"questions/by-solution/{solution_id}")
        return resp.json() if resp and resp.status_code == 200 else []

    def get_question(self, question_id):
        resp = self._request("GET", f"questions/{question_id}")
        return resp.json() if resp and resp.status_code == 200 else None

    def create_question(self, solution_id, body):
        payload = {"solution_id": solution_id, "body": body}
        resp = self._request("POST", "questions", json=payload)
        return resp.json() if resp and resp.status_code == 201 else None

    def answer_question(self, question_id, answer):
        resp = self._request("PATCH", f"questions/{question_id}", json={"answer": answer})
        return resp and resp.status_code == 200

    def generate_question_answer(self, question_id, persona="basis"):
        resp = self._request("POST", f"questions/{question_id}/generate", params={"persona": persona})
        if resp and resp.status_code == 200: return resp.json()
        if resp and resp.status_code == 402: Context.print_error(resp.json().get('detail'))
        return None

    def create_hint_draft(self, solution_id, notes):
        payload = {"solution_id": solution_id, "user_notes": notes}
        resp = self._request("POST", "hints/draft", json=payload)
        return resp.json() if resp and resp.status_code == 201 else None

    def generate_hint(self, hint_id, persona="basis"):
        resp = self._request("POST", f"hints/{hint_id}/generate", params={"persona": persona})
        if resp and resp.status_code == 200: return resp.json()
        if resp and resp.status_code == 402: Context.print_error(resp.json().get('detail'))
        return None

    def get_hints(self, solution_id):
        """Получает список подсказок для решения"""
        resp = self._request("GET", f"hints/by-solution/{solution_id}")
        return resp.json() if resp and resp.status_code == 200 else []

    def update_hint(self, hint_id, hint_text):
        """Обновляет текст подсказки"""
        payload = {"hint_text": hint_text}
        resp = self._request("PATCH", f"hints/{hint_id}", json=payload)
        return resp and resp.status_code == 200

class ContentApiMixin:
    """API для работы с контентом и OCR"""
    
    def trigger_problem_ocr(self, problem_id, persona="petrovich"):
        """Запуск распознавания условия задачи"""
        # Эндпоинт принимает query параметр persona для биллинга
        print(f"⏳ Запуск OCR задачи (AI {persona})... Ждите...")
        resp = self._request(
            "POST", 
            f"content/process-image/problem/{problem_id}", 
            params={"persona": persona}
        )
        if resp and resp.status_code == 200:
            data = resp.json()
            return data.get("text")
        elif resp and resp.status_code == 402:
            Context.print_error(f"Недостаточно средств: {resp.json().get('detail')}")
        elif resp:
            Context.print_error(f"Ошибка OCR: {resp.text}")
        return None

    def trigger_solution_ocr(self, solution_id, persona="petrovich"):
        """Запуск распознавания рукописного решения"""
        print(f"⏳ Запуск OCR задачи (AI {persona})... Ждите...")
        resp = self._request(
            "POST", 
            f"content/process-image/solution/{solution_id}", 
            params={"persona": persona}
        )
        if resp and resp.status_code == 200:
            data = resp.json()
            return data.get("text")
        elif resp and resp.status_code == 402:
            Context.print_error(f"Недостаточно средств: {resp.json().get('detail')}")
        elif resp:
            Context.print_error(f"Ошибка OCR: {resp.text}")
        return None


class ConceptsApiMixin:
    def analyze_problem(self, problem_id, persona="legendre"):
        resp = self._request("POST", f"concepts/analyze/problem/{problem_id}", params={"persona": persona})
        if resp and resp.status_code == 200: return resp.json()
        if resp and resp.status_code == 402: Context.print_error(resp.json().get('detail'))
        return None

    def analyze_solution(self, solution_id, persona="legendre"):
        resp = self._request("POST", f"concepts/analyze/solution/{solution_id}", params={"persona": persona})
        if resp and resp.status_code == 200: return resp.json()
        if resp and resp.status_code == 402: Context.print_error(resp.json().get('detail'))
        return None

    def deduplicate_concepts(self, persona="legendre"):
        resp = self._request("POST", "concepts/deduplicate", params={"persona": persona})
        return resp.json() if resp and resp.status_code == 200 else None

class BillingApiMixin:
    def get_billing_balance(self):
        resp = self._request("GET", "billing/balance")
        return resp.json() if resp and resp.status_code == 200 else None

    def create_topup(self, amount):
        resp = self._request("POST", "billing/top-up", params={"amount": amount})
        return resp.json() if resp and resp.status_code == 200 else None

class GamificationApiMixin:
    def get_gamification_me(self):
        """Получает текущий прогресс (XP, сердечки, страйк, количество решённых задач сегодня)"""
        resp = self._request("GET", "gamification/me")
        return resp.json() if resp and resp.status_code == 200 else None

    def get_daily_activity(self, days=7):
        """Получает статистику за последние N дней"""
        resp = self._request("GET", "gamification/activity/daily", params={"last_days": days})
        return resp.json() if resp and resp.status_code == 200 else None

class CommunityApiMixin:
    def get_articles(self, limit=10):
        resp = self._request("GET", "articles", params={"limit": limit})
        return resp.json() if resp and resp.status_code == 200 else []

class MindVectorAPI(BaseApiMixin, ProblemsApiMixin, SolutionsApiMixin, 
                    ArtifactsApiMixin, ConceptsApiMixin, BillingApiMixin, 
                    GamificationApiMixin, CommunityApiMixin, ContentApiMixin):
    pass