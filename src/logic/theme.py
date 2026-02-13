import flet as ft
from logic.file_handler import JsonFileHandler

class ThemeManager(JsonFileHandler):
    def __init__(self):
        super().__init__("themes.json", folder="assets")
        print(f"DEBUG: Looking for themes at: {self._path}")
        self.themes_data = self.load_json(default={"themes": {}})

    def get_themes(self):
        return self.themes_data.get("themes", {})
    
    def get_theme(self, theme_name):
        themes = self.get_themes()
        print(f"Themes: {themes}")
        data = themes.get(theme_name, list(themes.values())[0])  # Return first theme if not found
        
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                surface_tint=data["surface"],
                surface=data["surface"],
                primary=data["primary"],
                secondary=data["secondary"],
                on_primary=data["on_primary"],
                on_surface=data["on_surface"],
                outline=data["outline"]
            )
        )
    
    def get_background_color(self, theme_name):
        themes = self.get_themes()
        data = themes.get(theme_name, list(themes.values())[0])  # Return first theme if not found
        return data.get("background", "#FFFFFF")

theme_manager = ThemeManager()