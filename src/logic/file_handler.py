import sys
import json
from pathlib import Path

class JsonFileHandler:
    def __init__(self, filename, folder=None):
        self.filename = filename
        self.folder = folder
        self._path = self._resolve_path()
        
    def _resolve_path(self):
        if getattr(sys, 'frozen', False):
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).resolve().parent.parent
        
        if self.folder:
            return base_path / self.folder / self.filename
        else:
            return base_path / self.filename
    
    def load_json(self, default=None):
        if not self._path.exists():
            print(f"File not found at {self._path}. Returning default value.")
            return default if default is not None else {}
        
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {self.filename}: {e}")
            return default if default is not None else {}
    
    def save_json(self, data):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving {self.filename}: {e}")