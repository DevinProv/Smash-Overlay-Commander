import flet as ft
import threading
from components.counter import CounterInput
from logic.charmanager import char_manager


class PlayerCard(ft.Container):
    def __init__(self, player_num, initial_data=None, on_update=None, drag_handle=None):
        super().__init__()
        self.player_num = player_num
        self.on_update = on_update

        data = initial_data or {}

        self.score = data.get("score", 0)
        self.player_name = data.get("name", f"Player {player_num}")
        self.is_editing_name = False
        saved_char = data.get("character", None)
        saved_color = data.get("color", None)

        # Style
        self.border_radius = 15
        self.padding = 0
        self.width = 320
        self.height = 620
        self.border = ft.Border.all(1, "outlineVariant")
        self.gradient = ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[
                ft.Colors.with_opacity(0.1, "white"),
                ft.Colors.with_opacity(0.05, "white"),
            ],
        )
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.2, "black"),
            offset=ft.Offset(0, 5),
        )
        # Controls
        # Init Characters
        self.character_list = char_manager.get_character_names()

        self.score_display = ft.Text(
            str(self.score),
            size=32,
            weight="bold",
            font_family="monospace",
            scale=1.0,
            animate_scale=ft.Animation(100, ft.AnimationCurve.BOUNCE_OUT),
        )
        self.btn_minus = ft.IconButton(
            ft.Icons.REMOVE, icon_color="white70", on_click=self._decrement_score
        )
        self.btn_plus = ft.IconButton(ft.Icons.ADD, on_click=self._increment_score)

        self.score_container = ft.Container(
            bgcolor="#1A1A1A",
            border_radius=12,
            padding=5,
            border=ft.Border.all(1, ft.Colors.with_opacity(0.1, "white")),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[self.btn_minus, self.score_display, self.btn_plus],
            ),
        )
        self.name_input = ft.TextField(
            value=self.player_name,
            text_size=24,
            text_style=ft.TextStyle(weight="bold"),
            height=40,
            content_padding=5,
            expand=True,
            read_only=True,
            border_color="transparent",
            bgcolor="transparent",
            on_focus=self._on_name_focus,
            on_submit=self._save_name,
            on_blur=self._save_name,
        )
        self.name_wrapper = ft.Container(
            content=self.name_input,
            on_click=self._enable_name_edit,
            expand=True,
            padding=0,
        )
        
        handle_control = drag_handle if drag_handle else ft.Container()

        self.header_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    expand=True,
                    controls=[
                        handle_control,
                        ft.Container(width=10),
                        self.name_wrapper
                    ],
                )
            ],
        )

        initial_img_src = ""
        if saved_char and saved_color:
            initial_img_src = char_manager.get_asset_path(saved_char, saved_color)

        self.char_image = ft.Image(
            src=initial_img_src,
            width=250,
            height=250,
            fit="contain",
            opacity=1.0 if initial_img_src else 0,
        )
        self.glow_container = ft.Container(expand=True, border_radius=20, gradient=None)

        self.character_list = char_manager.get_character_names()
        self.char_dropdown = self._create_dropdown(
            hint="Character",
            value=saved_char,
            options=self.character_list,
            icon=ft.Icons.PERSON_OUTLINE,
            on_change=self._on_char_change,
        )
        self.color_dropdown = self._create_dropdown(
            hint="Color",
            value=saved_color,
            options=[],
            icon=ft.Icons.COLOR_LENS_OUTLINED,
            on_change=self._on_color_change,
            disabled=True,
        )

        self.ui_layer = ft.Container(
            padding=20,
            content=ft.Column(
                spacing=15,
                controls=[
                    self.header_row,
                    ft.Divider(height=1, color="white12"),
                    ft.Container(
                        content=self.char_image,
                        alignment=ft.Alignment.CENTER,
                        expand=True,
                    ),
                    ft.Column(
                        spacing=12,
                        controls=[
                            self.score_container,
                            self.char_dropdown,
                            self.color_dropdown,
                        ],
                    ),
                ],
            ),
        )

        self.content = ft.Stack(controls=[self.glow_container, self.ui_layer])

        if saved_char:
            self._load_colors_for_char(saved_char)
            self._update_card_border(
                saved_color if saved_color else "default", init_phase=True
            )
        else:
            self._update_card_border("default", init_phase=True)

    def _create_dropdown(self, hint, value, options, icon, on_change, disabled=False):
        opts = [
            ft.dropdown.Option(key=c, text=c.replace("_", " ").title()) for c in options
        ]
        return ft.Dropdown(
            hint_text=hint,
            value=value,
            options=opts,
            dense=True,
            height=45,
            text_size=14,
            border_radius=10,
            border_color="outline",
            filled=True,
            expand=True,
            bgcolor="black87",
            leading_icon=icon,
            on_select=on_change,
            disabled=disabled,
            content_padding=15,
        )

    def _load_colors_for_char(self, char):
        colors = char_manager.get_colors(char)
        self.color_dropdown.options = []
        for c in colors:
            clean_name = c.replace(".png", "").replace("_", " ").title()
            self.color_dropdown.options.append(
                ft.dropdown.Option(key=c, text=clean_name)
            )

        if colors:
            self.color_dropdown.disabled = False
        else:
            self.color_dropdown.disabled = True
    def _on_name_focus(self, e):
        self.name_input.read_only = False
        self.name_input.border_color = "outline"
        self.name_input.bgcolor = "surface"
        self.update()
    
    def _enable_name_edit(self, e):
        self.name_input.disabled = False
        self.name_input.border_color = "outline"
        self.name_input.bgcolor = "surface"
        
        self.update()
        self.name_input.focus()
    
    def _save_name(self, e):
        self.player_name = self.name_input.value
        self.name_input.read_only = True
        self.name_input.border_color = "transparent"
        self.name_input.bgcolor = "transparent"
        
        self._trigger_update("name", self.player_name)
        self.update()
    
    def _increment_score(self, e):
        self.score += 1
        self._update_score_display()

    def _decrement_score(self, e):
        if self.score > 0:
            self.score -= 1
            self._update_score_display()

    def _update_score_display(self):
        self.score_display.value = str(self.score)

        self.score_display.scale = 1.3
        self.score_display.update()

        def reset_scale():
            self.score_display.scale = 1.0
            self.score_display.update()

        threading.Timer(0.1, reset_scale).start()

        self._trigger_update("score", self.score)

    def _on_char_change(self, e):
        selected_char = self.char_dropdown.value
        self._load_colors_for_char(selected_char)

        colors = char_manager.get_colors(selected_char)
        if colors:
            default = next((c for c in colors if "default" in c), colors[0])
            self.color_dropdown.value = default
            self._update_image(selected_char, default)
            self._trigger_update("color", default)
        self.color_dropdown.update()
        self._trigger_update("character", selected_char)

    def _on_color_change(self, e):
        char = self.char_dropdown.value
        color = self.color_dropdown.value
        if char and color:
            self._update_image(char, color)
            self._trigger_update("color", color)
            self._update_card_border(color)

    def _update_card_border(self, color, init_phase=False):
        glow_color = None
        display_color = "outlineVariant"

        if color:
            raw_color = (
                color.replace(".png", "").replace(" ", "").lower()
                if color != "default"
                else "red"
            )
            if raw_color == "darkblue":
                raw_color = "#00008B"
            try:
                ft.Colors.with_opacity(1.0, raw_color)
                display_color = raw_color
                glow_color = raw_color if color != "default" else "default"
            except Exception:
                display_color = "cyan"
                glow_color = "cyan"
        self.border = ft.Border.all(2, display_color)

        if glow_color and glow_color != "default":
            self.glow_container.gradient = ft.RadialGradient(
                center=ft.Alignment(0, -0.4),
                radius=0.8,
                colors=[
                    ft.Colors.with_opacity(0.5, glow_color),
                    ft.Colors.with_opacity(0.1, glow_color),
                    ft.Colors.with_opacity(0.0, glow_color),
                ],
                stops=[0.0, 0.4, 1.0],
            )

        else:
            self.glow_container.gradient = None

        if not init_phase:
            self.glow_container.update()
            self.update()

    def _update_image(self, char, color_file):
        src = char_manager.get_asset_path(char, color_file)
        self.char_image.src = src
        self.char_image.opacity = 1
        if self.char_image.page:
            self.char_image.update()
            self._update_card_border(color_file)

    def _trigger_update(self, key, value):
        if self.on_update:
            self.on_update(self.player_num, key, value)

    def get_data(self):
        return {
            "name": self.player_name,
            "score": self.score,
            "character": self.char_dropdown.value,
            "color": self.color_dropdown.value,
        }

    def set_data(self, data):
        self.player_name = data.get("name", "Player")
        self.name_input.value = self.player_name

        self.score = int(data.get("score", 0))
        self.score_display.value = str(self.score)

        char = data.get("character")
        color = data.get("color")

        self.char_dropdown.value = char
        self._load_colors_for_char(char)

        if color in [opt.key for opt in self.color_dropdown.options]:
            self.color_dropdown.value = color
        else:
            self.color_dropdown.value = (
                self.color_dropdown.options[0].key
                if self.color_dropdown.options
                else None
            )

        self._update_image(char, self.color_dropdown.value)
        self._update_card_border(self.color_dropdown.value)

        self._trigger_update("name", self.player_name)
        self._trigger_update("score", self.score)
        self._trigger_update("character", char)
        self._trigger_update("color", color)

        self.update()
