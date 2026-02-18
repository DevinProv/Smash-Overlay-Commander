from logic.file_handler import JsonFileHandler

STATIC_KEYS = [
    "Round Title",
    "Tournament Title",
    "Scrolling Text",
    "Bracket URL",
    "Caster 1 Name",
    "Caster 2 Name",
    "Set Score",
]


class ConfigManager(JsonFileHandler):
    def __init__(self):
        
        super().__init__("config.json")
        self.config_file = "config.json"
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
        loaded_data = self.load_json(default={})
        
        if not loaded_data:
            self.save()
            return
        
        for key, val in loaded_data.items():
            if key != "mappings":
                self.data[key] = val

        supported_keys = self._generate_supported_keys()

        current_mappings = {k: None for k in supported_keys}

        saved_mappings = loaded_data.get("mappings", {})
        current_mappings.update(saved_mappings)

        clean_mappings = {
            k: v for k, v in current_mappings.items() if k in supported_keys
        }

        self.data["mappings"] = clean_mappings
        self.save()

    def save(self):
        self.save_json(self.data)
        
    def get_mapping(self, key):
        return self.data["mappings"].get(key)

    def update_mapping(self, new_map):
        self.data["mappings"].update(new_map)
        self.save()

    def get_supported_keys(self):
        return self._generate_supported_keys()

    def get_theme(self):
        return self.data.get("theme", "Moonlit Mist")

    def get_theme_list(self):
        theme_handler = JsonFileHandler("themes.json", folder="assets")
        
        data = theme_handler.load_json(default={})
        themes= data.get("themes", {})
        
        if not themes:
            return ["Moonlit Mist"]
        
        return list(themes.keys())
    
    
    def set_mapping(self, key, value):
        self.data["mappings"][key] = value
        self.save()



cfg = ConfigManager()
