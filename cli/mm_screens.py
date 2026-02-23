#!/usr/bin/env python3
"""
Mental Math Trainer - Screens
Экраны CLI приложения
"""
import time
from datetime import datetime
from mm_context import Context
from mm_api import MentalMathAPI


class ScreenManager:
    """Менеджер экранов CLI приложения."""
    
    def __init__(self, api: MentalMathAPI):
        self.api = api
        self.levels = []
    
    def ensure_auth(self) -> bool:
        """Проверка авторизации."""
        Context.print_header("🔐 АВТОРИЗАЦИЯ")
        
        # Попробовать существующий токен
        if self.api.token and self.api.get_me():
            nickname = self.api.user.get('nickname') or f"User #{self.api.user.get('id')}"
            print(f"👋 С возвращением, {nickname}!")
            return True
        
        # Регистрация по account_key
        if self.api.register():
            self.api.get_me()
            Context.print_success("Вход выполнен!")
            return True
        
        Context.print_error("Не удалось войти.")
        return False

    def flow_main_menu(self):
        """Главное меню."""
        # Загрузить уровни
        self.levels = self.api.get_levels()
        
        while True:
            progress = self.api.get_progress()
            
            Context.print_header("🧮 MENTAL MATH TRAINER")
            
            # Показать прогресс
            if progress:
                level = progress.get('current_level', 1)
                sub = progress.get('current_sub_level', 1)
                xp = progress.get('total_xp', 0)
                tasks = progress.get('total_tasks', 0)
                accuracy = progress.get('accuracy', 0)
                
                print(f"📊 Уровень: {level}.{sub} | XP: {xp} | Задач: {tasks} | Точность: {accuracy:.0f}%")
                print()
            
            print("1. 🎯 Тренировка")
            print("2. 📈 Выбор уровня")
            print("3. 📊 Статистика")
            print("4. 📜 История сессий")
            print("5. 👤 Профиль")
            print("0. 🚪 Выход")
            
            choice = input("\n> ").strip()
            
            if choice == '0':
                print("👋 До встречи!")
                break
            elif choice == '1':
                self.flow_training()
            elif choice == '2':
                self.flow_level_select()
            elif choice == '3':
                self.flow_statistics()
            elif choice == '4':
                self.flow_history()
            elif choice == '5':
                self.flow_profile()

    def flow_training(self):
        """Режим тренировки."""
        progress = self.api.get_progress()
        level = progress.get('current_level', 1) if progress else 1
        
        Context.print_header(f"🎯 ТРЕНИРОВКА - Уровень {level}")
        
        # Генерируем задачу
        Context.print_info("Генерация задачи...")
        task = self.api.generate_task(level)
        
        if not task:
            Context.print_error("Не удалось сгенерировать задачу.")
            input("\nEnter для продолжения...")
            return
        
        self._solve_task(task)

    def flow_level_select(self):
        """Выбор уровня."""
        if not self.levels:
            self.levels = self.api.get_levels()
        
        while True:
            Context.print_header("📈 ВЫБОР УРОВНЯ")
            
            for lv in self.levels:
                num = lv['level']
                name = lv['name']
                desc = lv['description']
                topics = ', '.join(lv['topics'][:3])
                print(f"{num}. {name}")
                print(f"   {desc}")
                print(f"   Темы: {topics}")
                print()
            
            print("0. Назад")
            
            choice = input("\nВыберите уровень (1-10): ").strip()
            
            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= 10:
                self._select_level_flow(int(choice))
            else:
                Context.print_error("Неверный выбор.")

    def _select_level_flow(self, level: int):
        """Флоу выбранного уровня."""
        while True:
            level_info = next((l for l in self.levels if l['level'] == level), None)
            if not level_info:
                break
            
            Context.print_header(f"📚 УРОВЕНЬ {level}: {level_info['name']}")
            print(f"{level_info['description']}")
            print()
            
            print("1. 🎯 Начать тренировку")
            print("2. 📋 Выбрать тему")
            print("0. Назад")
            
            choice = input("\n> ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._training_level(level)
            elif choice == '2':
                self._select_topic(level)

    def _select_topic(self, level: int):
        """Выбор темы."""
        level_info = next((l for l in self.levels if l['level'] == level), None)
        if not level_info:
            return
        
        topics = level_info['topics']
        
        while True:
            print(f"\n📋 ТЕМЫ УРОВНЯ {level}:")
            for idx, topic in enumerate(topics, 1):
                print(f"{idx}. {topic}")
            print("0. Назад")
            
            choice = input("\nВыберите тему: ").strip()
            
            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(topics):
                topic = topics[int(choice) - 1]
                self._training_level(level, topic=topic)

    def _training_level(self, level: int, topic: str = None):
        """Тренировка на уровне."""
        while True:
            Context.print_info(f"Генерация задачи (уровень {level})...")
            task = self.api.generate_task(level, topic=topic)
            
            if not task:
                Context.print_error("Не удалось сгенерировать задачу.")
                input("\nEnter...")
                break
            
            if not self._solve_task(task):
                break

    def _solve_task(self, task: dict) -> bool:
        """
        Решение задачи. Возвращает True если продолжить, False если выйти.
        """
        task_id = task['id']
        level = task['level']
        expr = Context.format_expression(task['expression'])
        
        Context.print_header(f"📝 ЗАДАЧА #{task_id} (Уровень {level})")
        print(f"\n    {expr}\n")
        print("─" * 50)
        
        # Таймер и подсказки
        start_time = time.time()
        hints_used = 0
        solution_steps = task.get('solution_steps', [])
        
        while True:
            print("\n[Enter] Ввести ответ | [h] Подсказка | [s] Пропустить | [q] Выход")
            cmd = input("> ").strip().lower()
            
            if cmd == 'q':
                return False
            
            elif cmd == 'h':
                hints_used += 1
                if hints_used <= len(solution_steps):
                    step = solution_steps[hints_used - 1]
                    print(f"\n💡 Подсказка {hints_used}: {step}")
                else:
                    print("\n💡 Больше подсказок нет.")
            
            elif cmd == 's':
                print(f"\n📤 Правильный ответ: {task['answer']}")
                print("Шаги решения:")
                for idx, step in enumerate(solution_steps, 1):
                    print(f"  {idx}. {step}")
                input("\nEnter для следующей задачи...")
                return True
            
            elif cmd == '':
                # Ввод ответа
                answer = input("Ваш ответ: ").strip()
                
                if not answer:
                    continue
                
                end_time = time.time()
                time_seconds = int(end_time - start_time)
                
                # Запрос ментальных шагов
                print("\n📊 Оцените решение:")
                mental_steps = Context.input_int("Ментальных шагов (в уме)", 1)
                written_steps = Context.input_int("Письменных шагов", 0)
                
                # Проверка ответа
                result = self.api.validate_answer(
                    task_id=task_id,
                    user_answer=answer,
                    mental_steps=mental_steps,
                    written_steps=written_steps,
                    time_seconds=time_seconds,
                    hints_used=hints_used
                )
                
                if result:
                    is_correct = result['is_correct']
                    xp = result['xp_earned']
                    correct_answer = result['correct_answer']
                    
                    print()
                    if is_correct:
                        Context.print_success(f"ПРАВИЛЬНО! +{xp} XP")
                    else:
                        Context.print_error(f"НЕВЕРНО!")
                        print(f"   Правильный ответ: {correct_answer}")
                    
                    print(f"   Время: {Context.format_time(time_seconds)}")
                    print(f"   Ментальных шагов: {mental_steps}, Письменных: {written_steps}")
                    
                    # Показать решение
                    if input("\nПоказать решение? (y/n): ").lower() == 'y':
                        print("\n📖 Шаги решения:")
                        for idx, step in enumerate(result['solution_steps'], 1):
                            print(f"  {idx}. {step}")
                
                input("\nEnter для следующей задачи...")
                return True
        
        return True

    def flow_statistics(self):
        """Экран статистики."""
        Context.print_header("📊 СТАТИСТИКА")
        
        # Прогресс
        progress = self.api.get_progress()
        if progress:
            level = progress.get('current_level', 1)
            sub = progress.get('current_sub_level', 1)
            xp = progress.get('total_xp', 0)
            tasks = progress.get('total_tasks', 0)
            correct = progress.get('correct_tasks', 0)
            streak = progress.get('streak_days', 0)
            accuracy = progress.get('accuracy', 0)
            next_xp = progress.get('next_level_xp', 100)
            
            print(f"📊 Текущий уровень: {level}.{sub}")
            print(f"⭐ Всего XP: {xp}")
            print(f"🔥 Стрик: {streak} дней")
            print()
            
            # Бар прогресса уровня
            level_progress = progress.get('level_progress', 0)
            bar = Context.draw_bar(level_progress, 100)
            print(f"📈 Прогресс уровня: {bar} {level_progress}%")
            print()
            
            print(f"✅ Решено задач: {tasks}")
            print(f"🎯 Правильных: {correct} ({accuracy:.1f}%)")
        
        # Статистика за неделю
        print("\n" + "─" * 50)
        print("📅 АКТИВНОСТЬ ЗА 7 ДНЕЙ\n")
        
        stats = self.api.get_stats(days=7)
        if stats:
            total = stats.get('total_sessions', 0)
            correct_s = stats.get('correct_sessions', 0)
            total_xp = stats.get('total_xp', 0)
            avg_time = stats.get('avg_time_seconds', 0)
            acc = stats.get('accuracy', 0)
            
            print(f"   Сессий: {total}")
            print(f"   Правильных: {correct_s} ({acc:.1f}%)")
            print(f"   Заработано XP: {total_xp}")
            print(f"   Среднее время: {avg_time:.1f} сек")
        else:
            print("   Нет данных за неделю.")
        
        input("\n\nEnter для продолжения...")

    def flow_history(self):
        """История сессий."""
        Context.print_header("📜 ИСТОРИЯ СЕССИЙ")
        
        sessions = self.api.get_sessions(limit=20)
        
        if not sessions:
            print("📭 История пуста.")
            input("\nEnter для продолжения...")
            return
        
        print(f"{'ID':<6} {'Уровень':<8} {'Ответ':<15} {'Результат':<12} {'XP':<6} {'Время'}")
        print("─" * 60)
        
        for s in sessions:
            sid = s['id']
            # Получаем уровень задачи из связанных данных (упрощенно)
            is_correct = s['is_correct']
            answer = s['user_answer'][:12] if s['user_answer'] else "-"
            result = "✅ Верно" if is_correct else "❌ Ошибка"
            xp = s['xp_earned']
            time_s = s['time_seconds']
            
            print(f"{sid:<6} {'?':<8} {answer:<15} {result:<12} {xp:<6} {time_s}с")
        
        input("\n\nEnter для продолжения...")

    def flow_profile(self):
        """Экран профиля."""
        Context.print_header("👤 ПРОФИЛЬ")
        
        user = self.api.get_me()
        if user:
            uid = user.get('id')
            nickname = user.get('nickname') or f"User #{uid}"
            created = user.get('created_at', '')[:10]
            
            print(f"ID: {uid}")
            print(f"Никнейм: {nickname}")
            print(f"Создан: {created}")
            
            account_key = Context.load_account_key()
            if account_key:
                print(f"\n🔑 Account Key: {account_key[:20]}...")
                print("   (Сохраните для входа на другом устройстве)")
        
        print("\n1. Сменить никнейм")
        print("0. Назад")
        
        choice = input("\n> ").strip()
        
        if choice == '1':
            new_name = input("Новый никнейм: ").strip()
            if new_name:
                # TODO: добавить endpoint для обновления профиля
                Context.print_info("Функция в разработке.")
        
        input("\nEnter для продолжения...")
