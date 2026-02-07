from pathlib import Path
import json
import flet as ft

CURRENT_DIR = Path(__file__).resolve().parent

THEME_FILE_PATH = CURRENT_DIR.parent / "assets" / "themes.json"


class ThemeManager:
    def __init__(self):
        self.themes = self._load_themes()

    def _load_themes(self):
        if not THEME_FILE_PATH.exists():
            print(f"Warning: Theme file not found at {THEME_FILE_PATH}")
            return self._get_fallback_theme()

        with open(THEME_FILE_PATH, "r") as f:
            return json.load(f)

    def get_theme_names(self):
        return list(self.themes.keys())

    def get_theme(self, theme_name):
        data = self.themes.get(theme_name, list(self.themes.values())[0])

        return ft.Theme(
            color_scheme=ft.ColorScheme(
                surface_tint=data["surface"],
                surface=data["surface"],
                primary=data["primary"],
                secondary=data["secondary"],
                on_primary=data["on_primary"],
                on_surface=data["on_surface"],
                outline=data["outline"],
            )
        )

    def get_background_color(self, theme_name):
        data = self.themes.get(theme_name, list(self.themes.values())[0])
        return data.get("background", "#111111")


theme_manager = ThemeManager()
