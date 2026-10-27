import webview
import os
import json
import sqlite3
import sys

# Get the folder where the .exe is located
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, 'app_data.db')
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
