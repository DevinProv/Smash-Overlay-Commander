import os
from logic.config import cfg

class CharacterManager:
    def __init__(self):
        self.data = {}
        self.char_dir = ""
        self._subscribers = []
        self.refresh()
    
    def register(self, card):
        if card not in self._subscribers:
            self._subscribers.append(card)
    
    def refresh(self):
        self.data = {}
        raw_path = cfg.data.get("character_assets_root", "characters")
        self.char_dir = os.path.abspath(raw_path)
        
        print(f"CharacterManager: Scanning {self.char_dir} for character assets...")
        
        if not os.path.exists(self.char_dir):
            print(f"Warning: Character directory not found at {self.char_dir}")
            return
        try:
            for char_name in os.listdir(self.char_dir):
                char_path = os.path.join(self.char_dir, char_name)

                if os.path.isdir(char_path):
                    colors = []
                    for file in os.listdir(char_path):
                        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                            colors.append(file)

                    colors.sort()

                    if colors:
                        self.data[char_name] = colors
        except Exception as e:
            print(f"Error refreshing character data: {e}")

        self.notify_subscribers()
    
    def notify_subscribers(self):
        print(f"Notifying {len(self._subscribers)} cards to update...")
        for card in self._subscribers:
            try:
                card.update_character_options()
            except Exception as e:
                print(f"Failed to update card: {e}")


    def get_character_names(self):
        return sorted(list(self.data.keys()))

    def get_colors(self, char_name):
        return self.data.get(char_name, [])

    def get_asset_path(self, char_name, color_filename):
        if not char_name or not color_filename:
            return os.path.join(self.char_dir, "placeholder.png")
        path = os.path.join(self.char_dir, char_name, color_filename)
        if os.path.exists(path):
            return path
        return os.path.join(self.char_dir, "placeholder.png")

char_manager = CharacterManager()
