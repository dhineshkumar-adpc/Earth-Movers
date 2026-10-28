import webview
import os
import json
import sqlite3
import sys
import shutil

# Get the folder where the .exe is located
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_documents_dir():
    """Real 'Documents' folder (follows OneDrive redirection). Works Windows 7 -> 11."""
    try:
        import ctypes
        from ctypes import wintypes
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)  # 5 = CSIDL_PERSONAL
        if buf.value:
            return buf.value
    except Exception:
        pass
    return os.path.join(os.path.expanduser('~'), 'Documents')

def get_data_dir():
    """Database lives in Documents\\FleetManagement (safe from uninstall/updates)."""
    try:
        path = os.path.join(get_documents_dir(), 'FleetManagement')
        os.makedirs(path, exist_ok=True)
        return path
    except Exception:
        path = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'FleetManagement')
        os.makedirs(path, exist_ok=True)
        return path

DB_PATH = os.path.join(get_data_dir(), 'app_data.db')

# One-time migration: copy old database from the app folder if it exists
_OLD_DB = os.path.join(BASE_DIR, 'app_data.db')
if os.path.exists(_OLD_DB) and not os.path.exists(DB_PATH):
    try:
        shutil.copy2(_OLD_DB, DB_PATH)
    except Exception:
        pass
# index.html is packed inside the .exe (PyInstaller --onefile), so users cannot edit it
RES_DIR = getattr(sys, '_MEIPASS', BASE_DIR)
HTML_FILE = os.path.join(RES_DIR, 'index.html')

class Api:
    def __init__(self):
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute('CREATE TABLE IF NOT EXISTS storage (key TEXT PRIMARY KEY, value TEXT)')
        conn.commit()
        conn.close()

    def save_data(self, data_json):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute('INSERT OR REPLACE INTO storage (key, value) VALUES (?, ?)', ('app_state', data_json))
            conn.commit()
            conn.close()
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def load_data(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.execute('SELECT value FROM storage WHERE key = ?', ('app_state',))
            row = cursor.fetchone()
            conn.close()
            return row[0] if row else None
        except Exception as e:
            return None

def start_app():
    api = Api()
    # Load the HTML file
    window = webview.create_window(
        'Dhineshkumar Adpc Murugan Trader - Fleet Management',
        HTML_FILE,
        js_api=api,
        width=1280,
        height=800,
        resizable=True
    )
    webview.start(debug=False)

if __name__ == '__main__':
    start_app()
