import datetime
import webbrowser
import sys
from mv_context import Context
from mv_api import MindVectorAPI

class ScreenManager:
    def __init__(self, api: MindVectorAPI):
        self.api = api

    # --- UI HELPERS ---
    
    def _draw_bar(self, value, max_val, width=15):
        """Рисует ASCII бар"""
        if max_val == 0: return ""
        bar_len = int((value / max_val) * width)
        return "█" * bar_len

    def _handle_ocr_and_edit(self, entity_type: str, entity_id: int, current_text: str = None, img_exists: bool = False):
        """
        Универсальный флоу: 
        1. Если текста нет и есть картинка -> Предложить OCR.
        2. Если текст есть (или получен через OCR) -> Открыть в браузере.
        3. Предложить сохранить правки.
        """
        target_text = current_text

        # 1. Логика OCR
        if not target_text and img_exists:
            print(f"\n🖼 У {entity_type} есть изображение, но нет текста.")
            if input("✨ Запустить AI Распознавание (OCR)? (y/n): ").lower() == 'y':
                persona = self._select_persona_interactive()
                
                # Вызываем соответствующий метод API
                if entity_type == 'problem':
                    target_text = self.api.trigger_problem_ocr(entity_id, persona)
                else:
                    target_text = self.api.trigger_solution_ocr(entity_id, persona)
                
                if target_text:
                    Context.print_success("Распознавание завершено!")
                    # Если нужно сохранить результат сразу в БД, API это уже сделал внутри trigger_...
                    # Но мы хотим дать возможность отредактировать.

        # 2. Если текст все еще пуст, и пользователь не захотел OCR или нет картинки
        if not target_text:
            print("ℹ️ Текст отсутствует.")
            if input("📝 Создать текст вручную? (y/n): ").lower() != 'y':
                return

        # 3. Открываем редактор
        Context.open_editor_browser(target_text or "")
        
        print("\n📝 Текст открыт в браузере.")
        print("Если вы внесли правки в браузере -> Нажмите кнопку COPY там и вставьте текст сюда.")
        print("Если правок нет -> Просто нажмите Enter.")
        
        print(f"\n↓↓↓ ВСТАВЬТЕ ТЕКСТ НИЖЕ (Ctrl+V) ↓↓↓")
        print("Для завершения ввода нажмите Enter на пустой строке дважды или введите 'END' на отдельной строке:")
        lines = []
        empty_line_count = 0
        
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                if line == "":
                    empty_line_count += 1
                    if empty_line_count >= 2:  # Two consecutive empty lines means end of input
                        lines.pop()  # Remove the last empty line
                        break
                    lines.append(line)
                else:
                    empty_line_count = 0
                    lines.append(line)
            except EOFError:
                break
        
        user_input = "\n".join(lines).strip()
        
        # 4. Сохранение
        if user_input:
            if entity_type == 'problem':
                self.api.update_problem_text(entity_id, user_input)
            else:
                self.api.update_solution_text(entity_id, user_input)
            Context.print_success("✅ Текст обновлен и сохранен!")
        else:
            print("👌 Оставлено без изменений (или использован результат OCR).")

    def _handle_question_answer_edit(self, question_id: int, current_answer: str = None):
        """
        Флоу для редактирования ответа на вопрос в браузере:
        1. Открыть текущий ответ (если есть) в браузере.
        2. Дать возможность отредактировать.
        3. Сохранить изменения.
        """
        target_text = current_answer or ""

        # Открываем редактор
        Context.open_editor_browser(target_text)

        print("\n📝 Ответ открыт в браузере.")
        print("Если вы внесли правки в браузере -> Нажмите кнопку COPY там и вставьте текст сюда.")
        print("Если правок нет -> Просто нажмите Enter.")

        print(f"\n↓↓↓ ВСТАВЬТЕ ТЕКСТ НИЖЕ (Ctrl+V) ↓↓↓")
        print("Для завершения ввода нажмите Enter на пустой строке дважды или введите 'END' на отдельной строке:")
        lines = []
        empty_line_count = 0

        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                if line == "":
                    empty_line_count += 1
                    if empty_line_count >= 2:  # Two consecutive empty lines means end of input
                        lines.pop()  # Remove the last empty line
                        break
                    lines.append(line)
                else:
                    empty_line_count = 0
                    lines.append(line)
            except EOFError:
                break

        user_input = "\n".join(lines).strip()

        # Сохранение
        if user_input:
            self.api.answer_question(question_id, user_input)
            Context.print_success("✅ Ответ обновлен и сохранен!")
        else:
            print("👌 Оставлено без изменений.")

    # --- SHARED COMPONENTS ---

    def _select_persona_interactive(self):
        """Интерактивный выбор персоны"""
        print("\n🤔 КОГО СПРОСИМ?")
        print("1. 🐱 Кот Базис    (Бесплатно, может лениться)")
        print("2. 🧹 Петрович     (2 ₽, Быстро, Gemini Flash)")
        print("3. 🧐 Лежандр      (10 ₽, Точно, Gemini Pro)")
        choice = input("Выберите (1-3) [2]: ").strip()
        if choice == '1': return "basis"
        if choice == '3': return "legendre"
        return "petrovich"

    def _select_tags_interactive(self):
        selected_tags = [] 
        print("\n🏷  ВЫБОР ТЕГОВ")
        print("Введите часть названия для поиска или полное имя для добавления.")
        print("Enter - закончить.")
        
        while True:
            current_names = [t['name'] for t in selected_tags]
            print(f"Выбрано: [{', '.join(current_names) or 'пусто'}]")
            user_input = input("Поиск/Добавление > ").strip()
            if not user_input: break
                
            matches = self.api.get_tags(search=user_input)
            exact_match = next((t for t in matches if t['name'].lower() == user_input.lower()), None)
            
            if exact_match:
                if exact_match not in selected_tags:
                    selected_tags.append(exact_match)
                    Context.print_success(f"Добавлен: {exact_match['name']}")
                else:
                    Context.print_info("Уже в списке.")
                continue
                
            if matches:
                print(f"Найдено {len(matches)}:")
                for idx, tag in enumerate(matches, 1):
                    marker = " [V]" if tag in selected_tags else ""
                    print(f"{idx}. {tag['name']}{marker}")
                print("0. Создать новый")
                
                sel = input("Выбор (0 для создания): ")
                if sel == '0':
                    selected_tags.append({"name": user_input})
                elif sel.isdigit() and 1 <= int(sel) <= len(matches):
                    tag = matches[int(sel)-1]
                    if tag not in selected_tags: selected_tags.append(tag)
            else:
                if input(f"Создать тег '{user_input}'? (y/n): ").lower() == 'y':
                    selected_tags.append({"name": user_input})

        return [t['name'] for t in selected_tags]

    # --- FLOWS ---

    def ensure_auth(self):
        Context.print_header("🔐 ВХОД В СИСТЕМУ")
        if self.api.token and self.api.get_me():
            print(f"👋 С возвращением, {self.api.user.get('username')}!")
            return True
        if self.api.device_login():
            Context.print_success("Вход по устройству выполнен")
            return True
        
        print("Требуется вход:")
        email = input("Email: ")
        pwd = input("Пароль: ")
        if self.api.login(email, pwd):
            Context.print_success("Успешный вход!")
            return True
        return False

    def flow_main_menu(self):
        user_info = self.api.get_me()
        is_admin = user_info and (user_info.get('role') == 'admin' or user_info.get('id') == 1)

        while True:
            Context.print_header("ГЛАВНОЕ МЕНЮ")
            print("1. 🚀 Решать задачу (Сессия)")
            print("2. 🧠 Анализ концепций")
            print("3. 📊 Статистика")
            print("4. 📂 Библиотека и Контент (OCR/Edit)")
            print("7. 💰 Финансы")
            print("8. 👤 Профиль")
            if is_admin: print("9. 🛠 Админка")
            print("0. Выход")
            
            c = input("> ")
            if c == '0': break
            elif c == '1': self.flow_solve_shortcut()
            elif c == '2': self.flow_concepts()
            elif c == '3': self.flow_statistics()
            elif c == '4': self.flow_library()
            elif c == '7': self.flow_finance()
            elif c == '8': self.flow_profile()
            elif c == '9' and is_admin: self.flow_admin()

    # --- НОВЫЙ РАЗДЕЛ: БИБЛИОТЕКА ---
    def flow_library(self):
        while True:
            Context.print_header("📂 БИБЛИОТЕКА И КОНТЕНТ")
            # 1. Выбор источника
            sources = self.api.get_sources()
            for idx, s in enumerate(sources, 1):
                print(f"{idx}. {s['name']}")
            print("0. Назад")
            
            choice = input("\nВыберите источник > ").strip()
            if choice == '0': break
            
            selected_source = None
            if choice.isdigit() and 1 <= int(choice) <= len(sources):
                selected_source = sources[int(choice)-1]['name']
            
            if not selected_source: continue

            # 2. Список задач источника
            while True:
                print(f"\n📄 ЗАДАЧИ: {selected_source}")
                problems = self.api.get_problems(source=selected_source)
                if not problems:
                    print("Задач пока нет.")
                    input("Enter...")
                    break
                    
                # Получаем список активных задач
                active_problem_ids = self._get_active_problem_ids()
                
                for p in problems:
                    icon = "📝" if p.get('condition_text') else "🖼️"
                    # Добавляем маркер активности, если задача активна
                    active_marker = "🟢" if p['id'] in active_problem_ids else ""
                    extra = self._format_problem_tags_concepts(p)
                    line = f"[{p['id']}] {icon} {p['reference']} {active_marker}"
                    if extra:
                        line += f"\n    {extra}"
                    print(line)
                
                pid_in = input("\nВведите ID задачи (или 0 назад): ")
                if pid_in == '0': break
                
                if pid_in.isdigit():
                    self._manage_problem_content(int(pid_in))

    def _format_problem_tags_concepts(self, p):
        """Формирует строку тегов и концепций для отображения в списке задач."""
        tags = p.get("tags") or []
        concepts = p.get("concepts") or []
        tag_names = [t.get("name", "") for t in tags if isinstance(t, dict) and t.get("name")]
        concept_names = [
            (c.get("concept") or {}).get("name", "")
            for c in concepts
            if isinstance(c, dict) and (c.get("concept") or {}).get("name")
        ]
        parts = []
        if tag_names:
            parts.append("🏷 " + ", ".join(tag_names))
        if concept_names:
            parts.append("💡 " + ", ".join(concept_names))
        return " | ".join(parts) if parts else ""

    def _get_active_problem_ids(self):
        """Получает список ID активных задач"""
        active_solutions = self.api.get_active_solutions()
        active_problem_ids = []
        for solution in active_solutions:
            problem_id = solution.get('problem_id')
            if problem_id:
                active_problem_ids.append(problem_id)
        return active_problem_ids

    def _manage_problem_content(self, problem_id):
        """Меню управления конкретной задачей"""
        while True:
            prob = self.api.get_problem(problem_id)
            if not prob:
                print("❌ Задача не найдена")
                return

            Context.print_header(f"🔧 ЗАДАЧА: {prob['reference']}")
            print(f"Источник: {prob['source']['name']}")
            print(f"Статус текста: {'✅ Есть' if prob.get('condition_text') else '❌ Нет'}")
            print(f"Статус фото: {'✅ Есть' if prob.get('condition_img') else '❌ Нет'}")

            print("\nДействия:")
            print("1. 👁 Просмотр/Редактирование/OCR Условия")
            print("2. 📂 Посмотреть решения к задаче")
            print("0. Назад")

            c = input("> ")
            if c == '0': break

            if c == '1':
                # Вызываем наш универсальный хелпер
                self._handle_ocr_and_edit(
                    'problem',
                    prob['id'],
                    prob.get('condition_text'),
                    bool(prob.get('condition_img'))
                )

            elif c == '2':
                self._manage_problem_solutions(problem_id)

    def _manage_problem_solutions(self, problem_id):
        """Список решений для задачи в режиме библиотеки"""
        while True:
            solutions = self.api.get_solutions(problem_id=problem_id)
            if not solutions:
                print("📭 Решений нет.")
                input("Enter...")
                return

            print(f"\n📂 РЕШЕНИЯ ({len(solutions)}):")
            for idx, s in enumerate(solutions, 1):
                status_icon = "✅" if s['status'] == 'completed' else "⏳"
                has_text = "📝" if s.get('solution_text') else "🖼️"
                print(f"{idx}. ID:{s['id']} {status_icon} {s['status']} {has_text} (XP: {s.get('xp_earned')})")
            
            print("0. Назад")
            c = input("Выберите номер решения > ")
            if c == '0': break
            
            if c.isdigit() and 1 <= int(c) <= len(solutions):
                sol = solutions[int(c)-1]
                # Управление контентом решения
                print(f"\n🔧 Решение ID {sol['id']}")
                self._handle_ocr_and_edit(
                    'solution',
                    sol['id'],
                    sol.get('solution_text'),
                    bool(sol.get('solution_img_path'))
                )

    # --- EXISTING FLOWS (Updated) ---

    def flow_solve_shortcut(self):
        # 1. Проверка активных
        active = self.api.get_active_solutions()
        sol_id = None
        existing_time = 0.0

        if active:
            print("\n--- АКТИВНЫЕ ЗАДАЧИ (Выбор для продолжения) ---")
            for idx, solution in enumerate(active, 1):
                prob = solution.get('problem', {})
                source = prob.get('source', {}).get('name', 'Unknown')
                ref = prob.get('reference', f"ID {solution['problem_id']}")
                print(f"{idx}. Продолжить: [{source}] {ref}")

            print(f"{len(active) + 1}. Новая задача")
            
            try:
                choice = int(input(f"Выберите (1-{len(active) + 1}): "))
                if 1 <= choice <= len(active):
                    selected_solution = active[choice - 1]
                    sol_id = selected_solution['id']
                    existing_time = selected_solution['total_minutes']
                elif choice == len(active) + 1:
                    # Создаем новую задачу
                    pass
                else:
                    print("Неверный выбор, создается новая задача...")
            except ValueError:
                print("Неверный ввод, создается новая задача...")

        # 2. Если нет активных или выбрана новая — создаем новую
        if not sol_id:
            pid = self._flow_select_task_for_solving() # Переименовал для ясности
            if pid:
                sol = self.api.create_solution(pid)
                if sol:
                    sol_id = sol['id']
                    existing_time = sol.get('total_minutes', 0.0)

        # 3. Старт сессии
        if sol_id:
            self.flow_solution_session(sol_id, existing_time)

    def _flow_select_task_for_solving(self):
        """Упрощенный выбор задачи чисто для старта решения"""
        print("\n--- БИБЛИОТЕКА ЗАДАЧ (Выбор для решения) ---")
        sources = self.api.get_sources()
        for idx, s in enumerate(sources, 1):
            print(f"{idx}. {s['name']}")
            
        choice = input("\nНомер источника, название нового или Enter (поиск): ").strip()
        selected_source = None
        
        if choice.isdigit() and 1 <= int(choice) <= len(sources):
            selected_source = sources[int(choice)-1]['name']
        elif choice:
            selected_source = choice

        problems = self.api.get_problems(source=selected_source)
        if problems:
            print(f"\nНайдены задачи ({len(problems)}):")
            # Получаем список активных задач
            active_problem_ids = self._get_active_problem_ids()
            
            for p in problems:
                icon = "📝" if p.get('condition_text') else "🖼️"
                # Добавляем маркер активности, если задача активна
                active_marker = "🟢" if p['id'] in active_problem_ids else ""
                extra = self._format_problem_tags_concepts(p)
                line = f"[{p['id']}] {icon} {p['source']['name']} - {p['reference']} {active_marker}"
                if extra:
                    line += f"\n    {extra}"
                print(line)
        else:
            print("Задач не найдено.")
        
        inp = input("\nID задачи или 'new' для создания: ")
        
        if inp.lower() == 'new':
            src = selected_source if selected_source else input("Источник: ")
            ref = input("Номер/Название: ")
            tags = self._select_tags_interactive()
            cond = input("Условие: ")
            prob = self.api.create_problem(ref, src, tags, cond)
            if prob:
                Context.print_success(f"Задача создана ID: {prob['id']}")
                if input("📸 Фото условия из буфера? (y/n): ").lower() == 'y':
                    path = Context.capture_clipboard_image()
                    if path: 
                        self.api.upload_image("condition", prob['id'], path)
                        Context.delete_file(path)
                        # Сразу предлагаем OCR
                        self._handle_ocr_and_edit('problem', prob['id'], cond, True)
                return prob['id']
            return None
        
        if inp.isdigit():
            # Перед стартом можно быстро глянуть условие
            prob = self.api.get_problem(int(inp))
            if prob:
                print(f"\nВыбрана: {prob['reference']}")
                if input("👁 Проверить/Распознать условие перед стартом? (y/n): ").lower() == 'y':
                     self._handle_ocr_and_edit(
                        'problem', 
                        prob['id'], 
                        prob.get('condition_text'), 
                        bool(prob.get('condition_img'))
                    )
                return prob['id']
                
        return None

    def flow_solution_session(self, solution_id, existing_minutes=0.0):
        start_time = datetime.datetime.now()
        Context.print_header(f"🚀 СЕССИЯ НАЧАТА: {start_time.strftime('%H:%M')}")
        print(f"Ранее потрачено: {existing_minutes:.1f} мин")
        print("Команды: [h]int, [e]piphany, [q]uestion, [s]tatus, [v]iew solution, [f]inish")
        
        while True:
            cmd = input("\nmv-session > ").lower().strip()
            if cmd == 'f': break
            
            elif cmd == 'v':
                # Просмотр/Редактирование текущего решения
                sol = self.api.get_solution(solution_id)
                self._handle_ocr_and_edit(
                    'solution', 
                    solution_id, 
                    sol.get('solution_text'), 
                    bool(sol.get('solution_img_path'))
                )
            
            elif cmd == 'e':
                desc = input("💡 Озарение: ")
                mag = Context.input_default("Сила (1-3)", "1")
                ep_data = self.api.create_epiphany(solution_id, desc, int(mag))
                if ep_data and input("📸 Схема из буфера? (y/n): ").lower() == 'y':
                     path = Context.capture_clipboard_image()
                     if path:
                         self.api.upload_image("epiphany", ep_data['id'], path)
                         Context.delete_file(path)
            elif cmd == 'q': self._handle_questions(solution_id)
            elif cmd == 'h': self._handle_hints_list(solution_id)
            elif cmd == 's':
                now = datetime.datetime.now()
                delta = (now - start_time).total_seconds() / 60
                print(f"⏱ Текущая сессия: {delta:.1f} мин")
                
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds() / 60
        Context.print_header(f"🛑 Сессия завершена ({duration:.1f} мин)")
        if self.api.post_session(solution_id, start_time, end_time, duration):
            Context.print_success("Время записано.")
            
        if input("🏁 Финализировать задачу? (y/n): ").lower() == 'y':
            diff = Context.input_default("Сложность (1-5)", "3")
            qual = Context.input_default("Качество (0.1-1.0)", "1.0")
            notes = input("Финальные заметки: ")
            
            if input("📸 Финальное фото решения? (y/n): ").lower() == 'y':
                path = Context.capture_clipboard_image()
                if path:
                    self.api.upload_image("solution", solution_id, path)
                    Context.delete_file(path)
                    print("✨ Рекомендуем распознать решение для архива.")
                    if input("Запустить OCR? (y/n): ").lower() == 'y':
                        self._handle_ocr_and_edit('solution', solution_id, None, True)

            res = self.api.finish_solution(solution_id, "completed", int(diff), float(qual), notes)
            if res: print(f"\n🏆 ЗАДАЧА ВЫПОЛНЕНА! Заработано XP: {res['xp_earned']}")

    def _handle_questions(self, solution_id):
        while True:
            print("\n❓ ВОПРОСЫ")
            qs = self.api.get_questions(solution_id)
            for q in qs:
                ans = "✅ " + q['answer'][:20] + "..." if q['answer'] else "❌"
                print(f"[{q['id']}] {q['body']} ({ans})")
            print("1. Новый\n2. Ответить вручную\n3. Спросить AI\n4. Редактировать ответ в браузере\n0. Назад")
            c = input("> ")
            if c == '1':
                body = input("Текст вопроса: ")
                q_data = self.api.create_question(solution_id, body)
                if q_data and input("📸 Фото контекста? (y/n): ").lower() == 'y':
                    path = Context.capture_clipboard_image()
                    if path:
                        self.api.upload_image("question", q_data['id'], path)
                        Context.delete_file(path)
            elif c == '2':
                qid = input("ID: ")
                ans = input("Ответ: ")
                self.api.answer_question(qid, ans)
            elif c == '3':
                qid = input("ID: ")
                if qid.isdigit():
                    persona = self._select_persona_interactive()
                    Context.print_info(f"Спрашиваю {persona}...")
                    res = self.api.generate_question_answer(int(qid), persona)
                    if res and res.get('answer'):
                        Context.open_editor_browser(res['answer'])
            elif c == '4':
                qid = input("ID вопроса для редактирования ответа: ")
                if qid.isdigit():
                    question = self.api.get_question(int(qid))
                    if question:
                        self._handle_question_answer_edit(int(qid), question.get('answer'))
                    else:
                        print("❌ Вопрос не найден")
            elif c == '0': break

    def _handle_hint(self, solution_id):
        print("\n🆘 СИСТЕМА ПОДСКАЗОК")
        notes = input("В чем проблема: ")
        hint_data = self.api.create_hint_draft(solution_id, notes)
        if not hint_data: return
        
        if input("📸 Прикрепить фото? (y/n): ").lower() == 'y':
            input("Скопируйте в буфер и Enter...")
            path = Context.capture_clipboard_image()
            if path:
                self.api.upload_image("hint", hint_data['id'], path)
                Context.delete_file(path)
                
        persona = self._select_persona_interactive()
        Context.print_info(f"Ждем ответа от {persona}...")
        res = self.api.generate_hint(hint_data['id'], persona)
        if res and res.get('hint_text'):
            Context.open_editor_browser(res['hint_text'])

    def _handle_hints_list(self, solution_id):
        """Список подсказок для решения"""
        while True:
            print("\n💡 ПОДСКАЗКИ")
            hints = self.api.get_hints(solution_id)
            if not hints:
                print("📭 Подсказок пока нет.")
                break

            for idx, h in enumerate(hints, 1):
                status_icon = "✅" if h.get('status') == 'completed' else "⏳"
                has_text = "📝" if h.get('hint_text') else "🖼️"
                print(f"{idx}. {status_icon} {has_text} (AI: {h.get('ai_model', 'N/A')})")

            print("1. 🆕 Создать новую")
            print("2. 📂 Посмотреть/Редактировать подсказку в браузере")
            print("0. Назад")

            c = input("> ")
            if c == '0': break
            elif c == '1':
                self._handle_hint(solution_id)
            elif c == '2':
                if not hints:
                    print("❌ Подсказок нет")
                    continue

                hint_num = input("Номер подсказки: ")
                if hint_num.isdigit() and 1 <= int(hint_num) <= len(hints):
                    hint = hints[int(hint_num) - 1]
                    self._handle_hint_edit(hint['id'], hint.get('hint_text'))
                else:
                    print("❌ Неверный номер")

    def _handle_hint_edit(self, hint_id, current_hint_text=None):
        """Флоу для редактирования подсказки в браузере"""
        target_text = current_hint_text or ""

        # Открываем редактор
        Context.open_editor_browser(target_text)

        print("\n📝 Подсказка открыта в браузере.")
        print("Если вы внесли правки в браузере -> Нажмите кнопку COPY там и вставьте текст сюда.")
        print("Если правок нет -> Просто нажмите Enter.")

        print(f"\n↓↓↓ ВСТАВЬТЕ ТЕКСТ НИЖЕ (Ctrl+V) ↓↓↓")
        print("Для завершения ввода нажмите Enter на пустой строке дважды или введите 'END' на отдельной строке:")
        lines = []
        empty_line_count = 0

        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                if line == "":
                    empty_line_count += 1
                    if empty_line_count >= 2:  # Two consecutive empty lines means end of input
                        lines.pop()  # Remove the last empty line
                        break
                    lines.append(line)
                else:
                    empty_line_count = 0
                    lines.append(line)
            except EOFError:
                break

        user_input = "\n".join(lines).strip()

        # Сохранение
        if user_input:
            self.api.update_hint(hint_id, user_input)
            Context.print_success("✅ Подсказка обновлена и сохранена!")
        else:
            print("👌 Оставлено без изменений.")

    def flow_statistics(self):
        """Экран статистики и активности"""
        Context.print_header("📊 СТАТИСТИКА И ПРОГРЕСС")
        
        # 1. Общие данные
        gamification = self.api.get_gamification_me()
        if gamification:
            xp = gamification.get('total_xp', 0)
            hearts = gamification.get('current_hearts', 5)
            streak = gamification.get('streak_current', 0)
            solved_tasks_today = gamification.get('solved_tasks_today', 0)
            print(f"⭐ XP: {xp:.1f} | ❤️ Сердца: {hearts}/5 | 🔥 Стрик: {streak} дн.")
            print(f"✅ Решено задач сегодня: {solved_tasks_today}")
        else:
            print("Не удалось загрузить данные профиля.")

        # 2. График активности
        print(f"\n📊 АКТИВНОСТЬ (7 дней)")
        print(f"{'Дата':<12} | {'Время':<6} | {'XP':<6} | {'График'}")
        print("-" * 50)

        activity = self.api.get_daily_activity(days=7)
        
        if activity and 'items' in activity:
            items = activity['items']
            today_str = datetime.date.today().isoformat()
            
            # Находим максимум для масштабирования
            max_xp = max((it['xp'] for it in items), default=1)
            if max_xp == 0: max_xp = 1
            
            valid_items = [it for it in items if it['xp'] > 0 or it['time_minutes'] > 0 or it['date'] == today_str]
            valid_items.sort(key=lambda x: x['date'])

            if not valid_items:
                print("📭 Нет данных.")
            else:
                for it in valid_items:
                    date_str = it['date']
                    mins = it['time_minutes']
                    xp_day = it['xp']
                    tasks_count = it.get('tasks_count', 0)  # Количество задач за день

                    bar = self._draw_bar(xp_day, max_xp)
                    day_label = "Сегодня" if date_str == today_str else date_str
                    print(f"{day_label:<12} | {mins:<6.0f} | {xp_day:<6.0f} | {bar} ({tasks_count} задач)")
            
            print("-" * 50)
            total_xp = activity.get('total_xp', 0)
            print(f"⭐️ ВСЕГО: {total_xp:.0f} XP")
        else:
            print("Нет данных.")
        input("\nEnter...")

    def flow_finance(self):
        while True:
            data = self.api.get_billing_balance()
            if not data: break
            
            bal = data.get('balance', 0.0)
            free = data.get('free_uses_left', 0)
            limit = data.get('total_daily_limit', 5)
            
            Context.print_header(f"💳 БАЛАНС: {bal:.2f} ₽")
            print(f"🐱 Кот Базис (Free): {free}/{limit} запросов")
            print("\n1. ➕ Пополнить баланс")
            print("2. 🔄 Обновить")
            print("0. 🔙 Назад")
            
            c = input("> ")
            if c == '0': break
            elif c == '1':
                try:
                    amt = float(input("Сумма (мин 10₽): "))
                    if amt >= 10:
                        res = self.api.create_topup(amt)
                        if res and 'payment_url' in res:
                            print(f"Ссылка: {res['payment_url']}")
                            if input("Открыть? (y/n): ").lower() == 'y':
                                webbrowser.open(res['payment_url'])
                            input("Нажмите Enter после оплаты...")
                except ValueError: pass

    def flow_concepts(self):
        Context.print_header("🧠 АНАЛИЗ КОНЦЕПЦИЙ")
        print("1. Анализ задачи (Карта Знаний)")
        print("2. Анализ решения (Трейс Навыков)")
        c = input("> ")
        if c == '1':
            pid = self._flow_select_task_for_solving() # Используем simple select
            if pid:
                persona = self._select_persona_interactive()
                res = self.api.analyze_problem(pid, persona)
                if res:
                    print("\n✅ Карта Знаний:")
                    for item in res:
                        print(f"- {item['concept']['name']} ({item['relevance']})")
        elif c == '2':
            # Выбор решения для анализа концепций
            print("\n🔍 ВЫБОР РЕШЕНИЯ ДЛЯ АНАЛИЗА")
            sources = self.api.get_sources()
            for idx, s in enumerate(sources, 1):
                print(f"{idx}. {s['name']}")
            
            choice = input("\nВыберите источник > ").strip()
            selected_source = None
            
            if choice.isdigit() and 1 <= int(choice) <= len(sources):
                selected_source = sources[int(choice)-1]['name']
            elif choice:
                # Если пользователь ввел название источника вручную
                selected_source = choice
            
            if selected_source:
                # Получаем задачи из выбранного источника
                problems = self.api.get_problems(source=selected_source)
                if problems:
                    print(f"\n📖 ЗАДАЧИ В ИСТОЧНИКЕ '{selected_source}':")
                    # Получаем список активных задач
                    active_problem_ids = self._get_active_problem_ids()
                    
                    for p in problems:
                        icon = "📝" if p.get('condition_text') else "🖼️"
                        # Добавляем маркер активности, если задача активна
                        active_marker = "🟢" if p['id'] in active_problem_ids else ""
                        extra = self._format_problem_tags_concepts(p)
                        line = f"[{p['id']}] {icon} {p['reference']} {active_marker}"
                        if extra:
                            line += f"\n    {extra}"
                        print(line)
                    
                    pid_input = input("\nВведите ID задачи > ").strip()
                    if pid_input.isdigit():
                        problem_id = int(pid_input)
                        # Получаем решения для выбранной задачи
                        solutions = self.api.get_solutions(problem_id=problem_id)
                        if solutions:
                            print(f"\n📂 РЕШЕНИЯ ДЛЯ ЗАДАЧИ {problem_id}:")
                            for idx, s in enumerate(solutions, 1):
                                status_icon = "✅" if s['status'] == 'completed' else "⏳"
                                has_text = "📝" if s.get('solution_text') else "🖼️"
                                print(f"{idx}. ID:{s['id']} {status_icon} {s['status']} {has_text} (XP: {s.get('xp_earned')})")
                            
                            sol_choice = input("\nВыберите ID решения для анализа > ").strip()
                            if sol_choice.isdigit():
                                solution_id = int(sol_choice)
                                # Проверяем, что решение принадлежит выбранной задаче
                                solution = next((s for s in solutions if s['id'] == solution_id), None)
                                if solution:
                                    persona = self._select_persona_interactive()
                                    # Вызываем API для анализа концепций из решения
                                    res = self.api.analyze_solution(solution_id, persona)
                                    if res:
                                        print("\n✅ Трейс Навыков:")
                                        for item in res:
                                            # Для SolutionConcept не выводим relevance, так как его там нет
                                            usage_context = item.get('usage_context', 'Контекст не указан')
                                            print(f"- {item['concept']['name']}: {usage_context}")
                                    else:
                                        print("❌ Не удалось получить анализ решения")
                                else:
                                    print("❌ Решение не найдено для этой задачи")
                            else:
                                print("❌ Неверный ID решения")
                        else:
                            print("📭 Нет решений для этой задачи")
                    else:
                        print("❌ Неверный ID задачи")
                else:
                    print("📭 Нет задач в этом источнике")
            else:
                print("❌ Неверный выбор источника")

    def flow_profile(self):
        user = self.api.get_me()
        print(f"\n👤 {user['username']} (ID: {user['id']})")
        if user.get('is_anonymous'):
            if input("Привязать Email? (y/n): ").lower() == 'y':
                email = input("Email: ")
                pwd = input("Пароль: ")
                username = input("Username: ")
                if self.api.link_email(email, pwd, username):
                    Context.print_success("Привязано!")
                else:
                    Context.print_error("Ошибка привязки")
        input("\nEnter для возврата...")

    def flow_admin(self):
        while True:
            Context.print_header("АДМИНКА")
            print("1. Объединить теги")
            print("2. Дедупликация концептов")
            print("0. Назад")
            c = input("> ")
            if c == '0': break
            if c == '1':
                target = input("Target Tag ID: ")
                sources = input("Source Tag IDs (comma): ")
                if target and sources:
                    self.api.merge_tags(int(target), [int(x) for x in sources.split(',')])
            if c == '2':
                self.api.deduplicate_concepts()