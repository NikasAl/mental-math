import os
import sys
import json
import uuid
import secrets
import tempfile
import webbrowser
from pathlib import Path
from PIL import ImageGrab

# --- КОНФИГУРАЦИЯ ---
API_URL = "http://localhost:8000/api/v1"
TOKEN_FILE = Path(".token")
DEVICE_CREDS_FILE = Path(".device_creds")

# HTML шаблон: Редактор + Live Preview + Кнопка копирования
HTML_EDITOR_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>MindVector Editor</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        MathJax = {
            tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] },
            svg: { fontCache: 'global' }
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { margin: 0; display: flex; height: 100vh; font-family: sans-serif; }
        .pane { width: 50%; padding: 20px; box-sizing: border-box; overflow-y: auto; }
        #editor-pane { background: #282c34; color: #abb2bf; border-right: 1px solid #ccc; display: flex; flex-direction: column; }
        #preview-pane { background: #fff; color: #333; }
        textarea { width: 100%; flex-grow: 1; background: transparent; color: inherit; border: none; outline: none; font-family: monospace; font-size: 14px; resize: none; }
        .toolbar { padding-bottom: 10px; border-bottom: 1px solid #444; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
        button { background: #61afef; border: none; padding: 8px 16px; color: white; cursor: pointer; border-radius: 4px; font-weight: bold; }
        button:hover { background: #4d8cc5; }
        h3 { margin: 0; color: #e06c75; }
    </style>
</head>
<body>
    <div class="pane" id="editor-pane">
        <div class="toolbar">
            <h3>Markdown Editor</h3>
            <button onclick="copyToClipboard()">📋 КОПИРОВАТЬ ДЛЯ ТЕРМИНАЛА</button>
        </div>
        <textarea id="source" oninput="updatePreview()"></textarea>
    </div>
    <div class="pane" id="preview-pane">
        <div id="preview-content"></div>
    </div>

    <div id="initial-content" style="display:none;"></div>

    <script>
        const source = document.getElementById('source');
        const preview = document.getElementById('preview-content');
        const initial = document.getElementById('initial-content').innerText;

        // Инициализация
        source.value = initial;
        updatePreview();

        function updatePreview() {
            preview.innerHTML = marked.parse(source.value);
            if (window.MathJax) {
                MathJax.typesetPromise([preview]).catch((err) => console.log(err));
            }
        }

        function copyToClipboard() {
            source.select();
            document.execCommand('copy');
            alert('Текст скопирован! Теперь вернитесь в терминал и вставьте его.');
        }
    </script>
</body>
</html>
"""

class Context:
    """
    Системный контекст: управление файлами, буфером обмена и выводом.
    """
    
    @staticmethod
    def load_token() -> str | None:
        if TOKEN_FILE.exists():
            return TOKEN_FILE.read_text().strip()
        return None

    @staticmethod
    def save_token(token: str):
        TOKEN_FILE.write_text(token)

    @staticmethod
    def get_or_create_device_creds():
        if DEVICE_CREDS_FILE.exists():
            try:
                data = json.loads(DEVICE_CREDS_FILE.read_text())
                return data['device_id'], data['secret']
            except Exception:
                pass 
        
        device_id = f"dev_{uuid.uuid4().hex[:12]}"
        secret = secrets.token_urlsafe(32)
        DEVICE_CREDS_FILE.write_text(json.dumps({"device_id": device_id, "secret": secret}))
        return device_id, secret

    @staticmethod
    def capture_clipboard_image() -> str | None:
        """Сохраняет картинку из буфера во временный файл и возвращает путь."""
        try:
            img = ImageGrab.grabclipboard()
            if img:
                fd, path = tempfile.mkstemp(suffix=".png")
                os.close(fd)
                img.save(path, "PNG")
                print(f"📸 Изображение захвачено: {path}")
                return path
            else:
                print("⚠️ Буфер обмена пуст.")
                return None
        except Exception as e:
            print(f"⚠️ Ошибка захвата буфера: {e}")
            return None

    @staticmethod
    def delete_file(path: str):
        if path and os.path.exists(path):
            os.remove(path)

    # --- UI HELPERS ---
    @staticmethod
    def open_editor_browser(text: str):
        """Открывает редактор текста в браузере"""
        try:
            fd, path = tempfile.mkstemp(suffix=".html")
            
            # Экранирование для вставки в HTML div
            safe_text = text.replace("<", "&lt;").replace(">", "&gt;")
            
            final_html = HTML_EDITOR_TEMPLATE.replace(
                '<div id="initial-content" style="display:none;"></div>', 
                f'<div id="initial-content" style="display:none;">{safe_text}</div>'
            )
            
            with os.fdopen(fd, 'w', encoding='utf-8') as tmp:
                tmp.write(final_html)
            
            print(f"🌍 Открываем редактор: {path}")
            webbrowser.open(f"file://{path}")
            
        except Exception as e:
            print(f"❌ Ошибка открытия браузера: {e}")

    # --- UI HELPERS ---
    
    @staticmethod
    def print_header(text: str):
        print(f"\n{'='*40}\n{text}\n{'='*40}")

    @staticmethod
    def print_success(text: str):
        print(f"✅ {text}")

    @staticmethod
    def print_error(text: str):
        print(f"❌ {text}")

    @staticmethod
    def print_info(text: str):
        print(f"ℹ️ {text}")
        
    @staticmethod
    def input_default(prompt: str, default: str) -> str:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default