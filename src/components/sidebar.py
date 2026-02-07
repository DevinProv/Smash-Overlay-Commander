import flet as ft

class Sidebar(ft.Container):
    def __init__(self, nav_rail, on_settings_click):
        super().__init__()
        self.nav_rail = nav_rail
        self.on_settings_click = on_settings_click

        self.bgcolor = "surface"
        self.padding = 0
        self.width = 100

        self.settings_btn = ft.Container(
            padding=ft.Padding.all(10),
            ink=True,
            on_click=self.on_settings_click,
            content=ft.Column([
                ft.Icon(ft.Icons.SETTINGS, color="on_surface_variant"),
                ft.Text("Settings", size=11, color="on_surface_variant")
            ],
            alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        self.content = ft.Column(
            expand=True,
            controls=[
            self.nav_rail,
            self.settings_btn
        ],
        spacing=0)