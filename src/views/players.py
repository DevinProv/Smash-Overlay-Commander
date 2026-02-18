import flet as ft
from logic.db_manager import db
from logic.charmanager import char_manager

class PlayersView(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = 20
        self.selected_player_name = None
        
        self.search_box = ft.TextField(
            hint_text="Search Players...",
            prefix_icon=ft.Icons.SEARCH,
            height=40,
            text_size=14,
            on_change=self._on_search_change
        )
        
        self.player_list = ft.ListView(
            expand=True,
            spacing=5,
            padding=10
        )

        self.left_panel = ft.Container(
            width=350,
            bgcolor="black26",
            padding=15,
            content=ft.Column([
                ft.Text("Player Directory", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, color="transparent"),
                self.search_box,
                ft.Divider(height=10, color="white10"),
                self.player_list
                ])
        )
        
        self.edit_name = ft.TextField(label="Player Name", read_only=True)
        self.edit_char = ft.Dropdown(label="Default Main",
                                     options=[ft.dropdown.Option(c) for c in char_manager.get_character_names()],
                                     on_select=self._on_edit_char_change
                                     )
        self.edit_color = ft.Dropdown(label="Default Color")
        
        self.stat_card = ft.Container(
            bgcolor="black26",
            padding=15,
            border_radius=10,
            content=ft.Column([
                ft.Text("Stats Coming Soon", size=16, weight=ft.FontWeight.BOLD, color="grey"),
                ft.Text("Matches Recorded: 0"),
                ft.Text("Win Rate: 0%")
            ])
        )
        
        self.detail_column = ft.Column(
            spacing=20,
            controls=[
                ft.Row([
                    ft.Icon(ft.Icons.EDIT, size=28),
                    ft.Text("Edit Player", size=28, weight=ft.FontWeight.BOLD)
                ]),
                ft.Divider(),
                self.edit_name,
                ft.Row([self.edit_char, self.edit_color]),
                self.stat_card,
                ft.Divider(),
                ft.Row(alignment=ft.MainAxisAlignment.END,
                       controls=[
                           ft.Button("Save Changes",
                                     icon=ft.Icons.SAVE,
                                     bgcolor=ft.Colors.BLUE_900,
                                     color=ft.Colors.WHITE,
                                     on_click=self._save_changes),
                           ft.TextButton("Delete",
                                         icon=ft.Icons.DELETE,
                                         icon_color=ft.Colors.RED,
                                         on_click=self._delete_player)
                       ])
        ])
        
        self.placeholder_msg = ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.PERSON, size=64, color="white24"),
                    ft.Text("Select a player to view details", color="white54")
                ]
            )
        )
        
        self.right_panel = ft.Container(
            expand=True,
            padding=30,
            bgcolor="black12",
            border_radius=10,
            content=self.placeholder_msg
        )
        
        self.content = ft.Row(spacing=20,
                              controls=[
                                  self.left_panel,
                                  self.right_panel
                              ])
        self._refresh_list(update_ui=False)
        
    def _refresh_list(self, query="", update_ui=True):
 
        self.player_list.controls.clear()
        players = db.search_players(query)
        
        for p in players:
            avatar = char_manager.get_asset_path(p['default_char'], p['default_color'])
            
            tile = ft.ListTile(
                leading=ft.CircleAvatar(
                    foreground_image_src=avatar if avatar else "",
                    content=ft.Text(p['name'][0] if not avatar else None),
                    bgcolor="blueGrey"
                ),
                title=ft.Text(p['name'], weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"{p['default_char']}"),
                on_click=lambda e, name=p['name']: self._select_player(name),
                hover_color="white10"
            )
            self.player_list.controls.append(tile)
        if update_ui:
            self.player_list.update()
        
    def _select_player(self, name):
        self.selected_player_name = name
        data = db.get_player(name)
        
        self.edit_name.value = data['name']
        self.edit_char.value = data['default_char']
        
        colors = char_manager.get_colors(data['default_char'])
        self.edit_color.options = [ft.dropdown.Option(c) for c in colors]
        self.edit_color.value = data['default_color']
        

        self.right_panel.content = self.detail_column
        self.right_panel.update()
    
    def _on_edit_char_change(self, e):
        char = self.edit_char.value
        colors = char_manager.get_colors(char)
        self.edit_color.options = [ft.dropdown.Option(c) for c in colors]
        if colors:
            self.edit_color.value = colors[0]
        self.edit_color.update()
        
    def _save_changes(self, e):
        db.upsert_player(
            self.edit_name.value,
            self.edit_char.value,
            self.edit_color.value
        )
        self._refresh_list(self.search_box.value)
        
    def _delete_player(self, e):
        if self.selected_player_name:
            db.delete_player(self.selected_player_name)
            self.selected_player_name = None

            self.right_panel.content = self.placeholder_msg
            self._refresh_list()
            self.update()
    
    def _on_search_change(self, e):
        self._refresh_list(self.search_box.value)
    
 