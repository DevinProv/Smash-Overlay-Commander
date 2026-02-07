import flet as ft
from logic.obs_manager import obs_manager


class MappingRow(ft.Container):
    def __init__(self, label_text, default_obs_source, source_options=[]):
        super().__init__()
        self.padding = ft.Padding.only(top=10, bottom=10, right=10)

        self.label = ft.Text(
            label_text, width=150, weight="bold", size=14, text_align="right"
        )

        dropdown_items = [
            ft.dropdown.Option(
                obs_manager.getKindEmoji(obs_manager.getInputKind(name)) + name
            )
            for name in source_options
        ]
        if default_obs_source is None or default_obs_source == "":
            emoji = ""
        else:
            emoji = obs_manager.getKindEmoji(
                obs_manager.getInputKind(default_obs_source)
            )
        self.obs_input = ft.Dropdown(
            options=dropdown_items,
            value=emoji + default_obs_source,
            label="Source",
            hint_text="Choose a source",
            height=40,
            text_size=14,
            content_padding=10,
            border_color="outlineVariant",
            dense=True,
            expand=True,
            autofocus=False,
            on_select=self.update_link_status,
        )
        
        self.content = ft.Row(
            controls=[
                self.label,
                ft.VerticalDivider(width=10, color="transparent"),
                self.obs_input,
                ft.Icon(ft.Icons.LINK_OFF, color="primary", size=20, tooltip="Linked"),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def get_data(self):
        return {
            "trigger": self.label.value,
            "obs_source": (
                self.obs_input.value[1:] if self.obs_input.value else None
            ),  # Remove emoji prefix
        }

    def update_link_status(self):
        if self.obs_input.value is None or self.obs_input.value == "":
            self.content.controls[3].icon = ft.Icons.LINK_OFF
            self.content.controls[3].color = "outlineVariant"
            self.content.controls[3].tooltip = "Not Linked"
            self.content.controls[2].border_color = "outlineVariant"
        else:
            self.content.controls[3].icon = ft.Icons.LINK
            self.content.controls[3].color = "primary"
            self.content.controls[3].tooltip = "Linked"
            self.content.controls[2].border_color = "outline"
        self.content.update()
