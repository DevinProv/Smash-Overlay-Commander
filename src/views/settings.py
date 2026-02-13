import flet as ft
from views.settings_sections import MappingSection
from views.settings_sections.general import GeneralSection

class SettingsView(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 20

        self.bgcolor = "surface"
        self.content_area = ft.Container(
            expand=True, padding=ft.Padding.symmetric(horizontal=30, vertical=20)
        )

        self.sections = {
            "General": GeneralSection,
            "Mapping": MappingSection,
        }
        self.nav_buttons = []
        for category in self.sections.keys():
            btn = self._create_nav_button(category)
            self.nav_buttons.append(btn)
        self.content = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(
                    border_radius=5,
                    width=200,
                    bgcolor="onSecondary",
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            ft.Container(
                                padding=20,
                                bgcolor="primary",
                                content=ft.Text(
                                    "Settings",
                                    size=24,
                                    weight="bold",
                                    color="onPrimary",
                                ),
                            ),
                            ft.Divider(height=1, thickness=1, color="outline"),
                            *self.nav_buttons,
                        ],
                        spacing=5,
                    ),
                ),
                ft.VerticalDivider(width=1, color="outline"),
                self.content_area,
            ],
            expand=True,
        )

        self._set_active_category("General", should_update=False)

    def _create_nav_button(self, text):
        return ft.Container(
            data=text,
            content=ft.Text(text, size=15, weight="w500"),
            padding=ft.Padding.all(12),
            border_radius=5,
            ink=True,
            on_click=self._on_nav_click,
            bgcolor=ft.Colors.TRANSPARENT,
            height=42,
            width=600,
        )

    def _on_nav_click(self, e):
        selected_category = e.control.data
        self._set_active_category(selected_category)

    def _set_active_category(self, category_name, should_update=True):
        for btn in self.nav_buttons:
            if btn.data == category_name:
                btn.bgcolor = "secondaryContainer"
                btn.content.color = "onSecondaryContainer"
            else:
                btn.bgcolor = ft.Colors.TRANSPARENT
                btn.content.color = "onSurface"

        content_generator = self.sections[category_name]

        self.content_area.content = content_generator()

        if should_update:

            self.update()



