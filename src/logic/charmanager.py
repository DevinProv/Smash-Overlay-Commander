import os


class CharacterManager:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.char_dir = os.path.join(project_root, "assets", "images")

        self.data = {}

        self.refresh()

    def refresh(self):
        self.data = {}

        if not os.path.exists(self.char_dir):
            print(f"Warning: Character directory not found at {self.char_dir}")
            return

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


    def get_character_names(self):
        return sorted(list(self.data.keys()))

    def get_colors(self, char_name):
        return self.data.get(char_name, [])

    def get_asset_path(self, char_name, color_filename):
        return f"assets/images/{char_name}/{color_filename}"


char_manager = CharacterManager()
