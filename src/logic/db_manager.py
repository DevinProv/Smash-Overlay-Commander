import sqlite3
import os
from datetime import datetime
from logic.config import cfg

class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(cfg.config_file), "smash_data.db")
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS players (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT UNIQUE NOT NULL,
                           default_char TEXT,
                           default_color TEXT,
                           created_at TEXT
                       )
                       ''')
        
        conn.commit()
        conn.close()
        
    def upsert_player(self, name, char, color):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id FROM players WHERE name = ?", (name,))
            data = cursor.fetchone()
            
            if data:
                cursor.execute('''
                               UPDATE players
                               SET default_char = ?, default_color = ?
                               WHERE name = ?
                               ''', (char, color, name))
            else:
                cursor.execute('''
                               INSERT INTO players (name, default_char, default_color, created_at)
                               VALUES (?, ?, ?, ?)
                               ''', (name, char, color, datetime.now().isoformat()))
            conn.commit()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    
    def get_player(self, name):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM players WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def search_players(self, query=""):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if query:
            cursor.execute("SELECT * FROM players WHERE name LIKE ? ORDER BY name", (f"%{query}%",))
        else:
            cursor.execute("SELECT * FROM players ORDER BY name")
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def delete_player(self, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM players WHERE name = ?", (name,))
        conn.commit()
        conn.close()

db = DatabaseManager()
