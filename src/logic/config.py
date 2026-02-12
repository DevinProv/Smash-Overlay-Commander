import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config.json")


STATIC_KEYS = [
    "Round Title",
    "Tournament Title",
    "Scrolling Text",
    "Bracket URL",
    "Caster 1 Name",
    "Caster 2 Name",
    "Set Score",
]


class ConfigManager:
    def __init__(self):
        self.default_settings = {
            "theme": "Moonlit Mist",
            "obs_host": "localhost",
            "obs_port": 4455,
            "obs_password": "",
            "min_players": 2,
            "max_players": 4,
            "mappings": {},
        }

        self.data = self.default_settings.copy()
        self.load()

    def _generate_supported_keys(self):
        keys = STATIC_KEYS.copy()

        count = self.data.get("max_players", 4)
        for i in range(1, count + 1):
            keys.append(f"Player {i} Name")
            keys.append(f"Player {i} Score")
            keys.append(f"Player {i} Character")
        return keys

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:

                    saved_data = json.load(f)

                    for key, val in saved_data.items():
                        if key != "mappings":
                            self.data[key] = val

                    supported_keys = self._generate_supported_keys()

                    current_mappings = {k: None for k in supported_keys}

                    saved_mappings = saved_data.get("mappings", {})
                    current_mappings.update(saved_mappings)

                    clean_mappings = {
                        k: v for k, v in current_mappings.items() if k in supported_keys
                    }

                    self.data["mappings"] = clean_mappings

            except Exception as e:
                print(f"Error loading config: {e}.")
                self.data["mappings"] = {
                    k: None for k in self._generate_supported_keys()
                }
        else:
            print("No config file found. Creating new one.")
            self.data["mappings"] = {k: None for k in self._generate_supported_keys()}
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
        return self._generate_supported_keys()

    def get_theme(self):
        return self.data.get("theme", "Moonlit Mist")

    def set_mapping(self, key, value):
        self.data["mappings"][key] = value
        self.save()



cfg = ConfigManager()
