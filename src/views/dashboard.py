import flet as ft
from components.matchsettings import MatchSettingsCard


class DashboardView(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = 30
        
        self.content = ft.Column(
            scroll="auto",
            controls=[
                ft.Text("Dashboard", size=30),
                MatchSettingsCard()
            ]
        )
