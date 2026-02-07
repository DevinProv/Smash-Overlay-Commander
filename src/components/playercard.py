import flet as ft
from components.counter import CounterInput
from logic.charmanager import char_manager

class PlayerCard(ft.Container):
    def __init__(self, player_num, initial_data=None, on_update=None):
        super().__init__()
        self.player_num = player_num
        self.on_update = on_update
        
        data = initial_data or {}
        
        self.score = data.get("score", 0)
        self.player_name = data.get("name", f"Player {player_num}")
        self.is_editing_name = False
        saved_char = data.get("character", None)
        saved_color = data.get("color", None)
        
        #Style
        self.bgcolor = "surfaceVariant"
        self.border_radius = 10
        self.padding = 15
        self.width = 300
        self.height=600
        self.border = ft.Border.all(1, "outlineVariant")

        #Controls
        #Init Characters
        self.character_list = char_manager.get_character_names()
        
        self.score_display = ft.Text(str(self.score), size=24, weight="bold")
        self.score_counter = CounterInput(
            value=self.score,
            min_value=0,
            max_value=999,
            on_change=lambda val: self._trigger_update("score", val),
            text_size=28
        )
        self.btn_minus = ft.IconButton(ft.Icons.REMOVE, on_click=self._decrement_score)
        self.btn_plus = ft.IconButton(ft.Icons.ADD, on_click=self._increment_score)
        
        self.name_display = ft.Text(self.player_name, size=24, weight="bold", expand=True)
        self.name_input = ft.TextField(
            value=self.player_name,
            height=30,
            text_size=20,
            content_padding=5,
            expand=True,
            on_submit=self._toggle_name_edit,
            visible=False,
            border_color="outline",
        )
        self.edit_icon = ft.IconButton(ft.Icons.EDIT, tooltip="Edit Name", icon_size=16, on_click=self._toggle_name_edit)
        
        self.header_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    expand=True,
                    controls=[self.name_display, self.name_input]
                ),
                self.edit_icon
            ]
        )
        
        initial_img_src = "assets/images/mario/default.png"
        if saved_char and saved_color:
            initial_img_src = char_manager.get_asset_path(saved_char, saved_color)
        self.char_image = ft.Image(
            #TODO Replace with default character image or blank
            src=initial_img_src,
            width=150,
            height=150,
            fit="contain"
        )
        
        self.char_dropdown = ft.Dropdown(
            hint_text="Character",
            value = saved_char,
            options=[
                ft.dropdown.Option(key=c,
                                   text=c.replace("_"," ").title()
                                   ) for c in self.character_list
                ],
            dense=True,
            height=45,
            text_size=14,
            border_radius=10,
            border_color="outline",
            filled=True,
            expand=True,
            bgcolor="surface",
            leading_icon=ft.Icons.PERSON_OUTLINE,
            on_select=self._on_char_change
        )
        
        self.color_dropdown = ft.Dropdown(
            hint_text="Color",
            value=saved_color,
            #TODO Handle Color Options based on char image folders
            options=[],
            dense=True,
            height=45,
            text_size=14,
            border_radius=10,
            border_color="outline",
            filled=True,
            expand=True,
            bgcolor="surface",
            leading_icon=ft.Icons.COLOR_LENS_OUTLINED,
            disabled=True,
            on_select=self._on_color_change
        )
        
        self.content = ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(controls=[self.name_display, self.name_input], expand=True),
                        self.edit_icon
                    ]
                ),
                ft.Divider(height=1, color="outlineVariant"),
                ft.Container(
                    content=self.char_image,
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                    padding=ft.Padding.symmetric(vertical=20)
                ),
                ft.Container(
                    bgcolor="surface",
                    border_radius=8,
                    padding=5,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[self.btn_minus, self.score_display, self.btn_plus],
                        spacing=5
                    )
                ),
                ft.Column(
                    spacing=10,
                    horizontal_alignment = ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        self.char_dropdown,
                        self.color_dropdown
                    ]
                ),
                ft.Container(height=15)
            ]
        )
        
        if saved_char:
            self._load_colors_for_char(saved_char)
            if saved_color:
                self.border, self.shadow = self._get_border_and_shadow(saved_color)
                
    def  _load_colors_for_char(self, char):
        colors = char_manager.get_colors(char)
        self.color_dropdown.options = []
        for c in colors:
            clean_name = c.replace(".png","").replace("_"," ").title()
            self.color_dropdown.options.append(
                ft.dropdown.Option(key=c, text=clean_name)
            )
        
        if colors:
            self.color_dropdown.disabled = False
        else:
            self.color_dropdown.disabled = True 
    
    def _get_border_and_shadow(self, color_filename):
        if not color_filename:
            return ft.Border.all(1, "outlineVariant"), None
        
        raw_color_name = color_filename.replace(".png","").lower()
        
        if raw_color_name == "default":
            display_color = "outlineVariant"
            shadow_color = None
        else:
            display_color = raw_color_name
            shadow_color = display_color
        
        try:
            border = ft.Border.all(2, display_color)
        except:
            border = ft.Border.all(2, "cyan")
            if raw_color_name != "default":
                shadow_color = "cyan"

        shadow = None
        if shadow_color:
            shadow = ft.BoxShadow(
                spread_radius=0,
                blur_radius=20,
                color=shadow_color,
                blur_style=ft.BlurStyle.OUTER
            )
        return border, shadow
    
    def _toggle_name_edit(self, e):
        self.is_editing_name = not self.is_editing_name
        
        if self.is_editing_name:
            self.name_display.visible = False
            self.name_input.visible = True
            self.name_input.value = self.player_name
            self.name_input.focus()
            self.edit_icon.icon = ft.Icons.CHECK
        else:
            self.player_name = self.name_input.value
            self.name_display.value = self.player_name
            self.name_display.visible = True
            self.name_input.visible = False
            self.edit_icon.icon = ft.Icons.EDIT
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
        self.update()
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
            
    def _update_card_border(self, color):
        self.border, self.shadow = self._get_border_and_shadow(color)
        if self.page:
            self.update()

    def _update_image(self, char, color_file):
        src = char_manager.get_asset_path(char, color_file)
        self.char_image.src = src
        if self.char_image.page:
            self.char_image.update()
    
    def _trigger_update(self, key, value):
        if self.on_update:
            self.on_update(self.player_num, key, value)
        
        