import flet as ft
from logic.config import cfg
from logic.theme import theme_manager 

class GeneralSection(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = 20
        
        # --- Appearance ---
        self.theme_dropdown = ft.Dropdown(
            label="Theme",
            leading_icon=ft.Icons.PALETTE,
            value=cfg.get_theme(),
            options=[ft.dropdown.Option(t) for t in cfg.get_theme_list()],
            on_select=self.on_theme_change, # Dropdowns are fine on_change
        )

        # --- OBS Settings ---
        self.obs_host_field = ft.TextField(
            label="OBS Host",
            prefix_icon=ft.Icons.COMPUTER,
            value=cfg.data.get("obs_host", "localhost"),
            on_blur=self.save_field_data, # Save only when done typing
            data="obs_host", # Store the config key in the control's data
        )
        
        self.obs_port_field = ft.TextField(
            label="OBS Port",
            prefix_icon=ft.Icons.CABLE,
            value=str(cfg.data.get("obs_port", 4455)),
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
            on_blur=self.validate_and_save_port,
        )
        
        self.obs_password_field = ft.TextField(
            label="OBS Password",
            prefix_icon=ft.Icons.LOCK,
            value=cfg.data.get("obs_password", ""),
            password=True,
            can_reveal_password=True,
            on_blur=self.save_field_data,
            data="obs_password",
        )
        
        self.test_connection_btn = ft.IconButton(
            icon=ft.Icons.WIFI,
            tooltip="Test OBS Connection",
            on_click=self.test_obs_connection,
            icon_color=ft.Colors.BLUE_700,
        )
        
        # --- Player Settings ---
        self.min_players_field = ft.TextField(
            label="Min Players",
            value=str(cfg.data.get("min_players", 2)),
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
            on_blur=self.validate_players,
            expand=True
        )
        
        self.max_players_field = ft.TextField(
            label="Max Players",
            value=str(cfg.data.get("max_players", 4)),
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
            on_blur=self.validate_players,
            expand=True
        )

        # --- Layout ---
        self.content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("General Settings", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                
                self._build_section(
                    "Appearance", 
                    "Theme and visual settings", 
                    [self.theme_dropdown]
                ),
                
                self._build_section(
                    "OBS Connection", 
                    "Configure WebSocket connection", 
                    [
                        self.obs_host_field, 
                        ft.Row([self.obs_port_field, self.obs_password_field, self.test_connection_btn])
                    ]
                ),
                
                self._build_section(
                    "Player Settings", 
                    "Configure bracket limits", 
                    [
                        ft.Row([self.min_players_field, self.max_players_field]),
                        ft.Container(
                            content=ft.Text(
                                "Note: Changing max players will regenerate mapping keys.",
                                size=12, italic=True, color=ft.Colors.AMBER,
                            ),
                            padding=ft.Padding.only(top=5),
                        ),
                    ]
                ),
                
                ft.Container(
                    padding=ft.Padding.only(top=20),
                    content=ft.FilledButton(
                        "Reset to Defaults",
                        icon=ft.Icons.RESTORE,
                        style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_700),
                        on_click=self.reset_to_defaults,
                    ),
                ),
            ],
        )

    def _build_section(self, title, subtitle, controls):
        """Helper to create consistent sections"""
        return ft.ExpansionTile(
            title=ft.Text(title, weight=ft.FontWeight.W_500),
            subtitle=ft.Text(subtitle, size=12, opacity=0.8),
            expanded=True, # 'expanded' is deprecated in newer Flet, use initially_expanded
            controls=[
                ft.Container(
                    content=ft.Column(controls=controls, spacing=15),
                    padding=ft.Padding.all(15),
                )
            ],
        )

    # --- Event Handlers ---
    def _apply_theme(self, theme_name):
        cfg.data["theme"] = theme_name
        cfg.save()
        
        if self.page:
            self.page.theme = theme_manager.get_theme(theme_name)
            self.page.bgcolor = theme_manager.get_background_color(theme_name)
            self.page.update()
    
    def test_obs_connection(self, e):
        from logic.obs_manager import obs_manager
        self.test_connection_btn.icon = ft.Icons.HOURGLASS_EMPTY
        self.test_connection_btn.update()
        
        success = obs_manager.test_connection(
            host = self.obs_host_field.value,
            port = int(self.obs_port_field.value),
            password = self.obs_password_field.value
        )
        if success:
            self.show_snackbar("Successfully connected to OBS!", ft.Colors.GREEN)
            self.test_connection_btn.icon = ft.Icons.CHECK_CIRCLE
            self.test_connection_btn.icon_color = ft.Colors.GREEN_700
        else:
            self.show_snackbar("Failed to connect to OBS. Check your settings.", ft.Colors.RED)
            self.test_connection_btn.icon = ft.Icons.ERROR
            self.test_connection_btn.icon_color = ft.Colors.RED_700
        self.test_connection_btn.update()
    
    def on_theme_change(self, e):
        self._apply_theme(e.control.value)
        self.show_snackbar(f"Theme changed to {e.control.value}", ft.Colors.GREEN)

    def save_field_data(self, e):
        """Generic saver for simple text fields using the 'data' property"""
        key = e.control.data
        if key:
            cfg.data[key] = e.control.value
            cfg.save()

    def validate_and_save_port(self, e):
        try:
            port = int(e.control.value)
            if 1 <= port <= 65535:
                cfg.data["obs_port"] = port
                cfg.save()
            else:
                raise ValueError
        except ValueError:
            e.control.value = str(cfg.data.get("obs_port", 4455))
            e.control.update()
            self.show_snackbar("Port must be 1-65535", ft.Colors.RED)

    def validate_players(self, e):
        """Validates both min and max players together"""
        try:
            min_p = int(self.min_players_field.value)
            max_p = int(self.max_players_field.value)
            
            if min_p > max_p:
                self.show_snackbar("Min players cannot exceed Max players", ft.Colors.RED)
                # Revert to config values
                self.min_players_field.value = str(cfg.data.get("min_players"))
                self.max_players_field.value = str(cfg.data.get("max_players"))
                self.update()
                return

            # Check if Max Players actually changed (requires regen)
            old_max = cfg.data.get("max_players")
            
            cfg.data["min_players"] = min_p
            cfg.data["max_players"] = max_p
            cfg.save()
            
            if max_p != old_max:
                cfg.load() # Trigger regen logic in ConfigManager
                self.show_snackbar("Player limits updated & mappings regenerated", ft.Colors.GREEN)
            
        except ValueError:
             self.show_snackbar("Invalid player numbers", ft.Colors.RED)

    def reset_to_defaults(self, e):
        # Reset data to the defaults defined in ConfigManager
        cfg.data = cfg.default_settings.copy()
        cfg.save()
        cfg.load() # Re-runs the load logic/cleaning
        
        # Update UI Controls
        self.theme_dropdown.value = cfg.data["theme"]
        self.obs_host_field.value = cfg.data["obs_host"]
        self.obs_port_field.value = str(cfg.data["obs_port"])
        self.obs_password_field.value = cfg.data["obs_password"]
        self.min_players_field.value = str(cfg.data["min_players"])
        self.max_players_field.value = str(cfg.data["max_players"])
        
        # Trigger the theme update so the user sees the reset visually
        self._apply_theme(cfg.data["theme"])
        
        self.update()
        self.show_snackbar("All settings reset to defaults", ft.Colors.GREEN)

    def show_snackbar(self, message, color):
        if self.page:
            self.page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
            self.page.snack_bar.open = True
            self.page.update()