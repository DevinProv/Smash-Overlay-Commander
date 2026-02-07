import flet as ft
from logic.theme import theme_manager

class ReplaysView(ft.Container):
    def __init__(self):
        super().__init__()
        self.bgcolor = "surface"
        self.content = ft.Text("Replays View!")
    