import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config.json")



SUPPORTED_KEYS = [
    "Player 1 Name", "Player 1 Score", "Player 1 Char",
    "Player 2 Name", "Player 2 Score", "Player 2 Char",
    "Round Title", "Tournament Title", "Scrolling Text",
    "Bracket URL", "Caster 1", "Caster 2",
    "Set Score", "Match Score"
]

class ConfigManager:
    def __init__(self):
        self.defaults = {
            "theme": "Moonlit Mist",
            "obs_password": "",
            "min_players": 2,
            "max_players": 4,
            "mappings": dict.fromkeys(SUPPORTED_KEYS, None)
        }

        self.data = self.defaults.copy()
        self.load()
    
    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                
                    saved_data = json.load(f)
                    self.data.update(saved_data)

                    saved_mappings = saved_data.get("mappings", {})
                    full_mappings = self.defaults["mappings"].copy()
                    full_mappings.update(saved_mappings)
                    self.data["mappings"] = full_mappings

                needs_save = False
                for key in self.defaults:
                    if key not in saved_data:
                        print(f"Migrating config: Adding missing key '{key}' with default value.")
                        needs_save = True
                if needs_save:
                    self.save()
                    
            except Exception as e:
                print(f"Error loading config: {e}.")
            else:
                self.save()
                
    def save(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}.")
    
    def get_mapping(self, key):
        return self.data["mappings"].get(key)
    
    def update_mapping(self, new_map):
        self.data["mappings"].update(new_map)
        self.save()
    
    def get_supported_keys(self):
        return SUPPORTED_KEYS
    
    def get_theme(self):
        return self.data.get("theme", "Moonlit Mist")
cfg = ConfigManager()