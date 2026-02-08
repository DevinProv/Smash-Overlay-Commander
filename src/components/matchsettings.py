import os
import flet as ft
from components.counter import CounterInput
from components.playercard import PlayerCard
from logic.config import cfg
from logic.obs_manager import obs_manager

class MatchSettingsCard(ft.Container):
    def __init__(self):
        super().__init__()
        
        self.expand = True
        self.padding = 0

        self.player_states = {}
        
        min_p = cfg.data.get("min_players", 2)
        max_p = cfg.data.get("max_players", 4)
        self.player_count = CounterInput(
            value=2, min_value=min_p, max_value=max_p, text_size=18, on_change=self._on_player_count_change
        )

        self.match_title = ft.TextField(
            hint_text="e.g. Winners Finals",
            border_radius=8,
            content_padding=12,
            text_size=14,
            height=45,
            expand=True,
        )
        self.reset_btn = ft.IconButton(ft.Icons.REFRESH, icon_color=ft.Colors.RED_800, tooltip="Reset Player Data", on_click=self._reset_player_data)
        self.cards_row = ft.Row(
            wrap=True,spacing=30, run_spacing=30, alignment=ft.MainAxisAlignment.CENTER, run_alignment=ft.MainAxisAlignment.CENTER
        )

        self._generate_cards(2)

        self.content = ft.Column(
            spacing=20,
            controls=[
                # Row 1 Player Count | Match Title
                ft.Divider(height=10, color="outline"),
                ft.Row(
                    spacing=20,
                    controls=[
                        self._input_group("Player Count", self.player_count),
                        self._input_group("Match Title", self.match_title),
                    ],
                ),
                ft.Divider(height=10, color="transparent"),
                ft.Row(
                    controls=[ft.Text("Player Controls", size=14, color="outline", weight="bold"),
                    self.reset_btn]
                ),
                ft.Container(expand=True, alignment=ft.Alignment.CENTER, content=self.cards_row)
                
            ],
        )

    def _input_group(self, label, control):
        return ft.Column(
            spacing=5,
            expand=label == "Match Title",
            controls=[
                ft.Text(label, size=12, weight="w500", color="outline"),
                control,
            ],
        )
    def _on_player_count_change(self, new_value):
        self._generate_cards(new_value)
        self.cards_row.update()
    
    def _generate_cards(self, count):
        self.cards_row.controls.clear()
        
        #TODO Implement Character List from Files
        
        for i in range(1, count + 1):
            saved_data = self.player_states.get(i, {})
            
            card = PlayerCard(
                player_num=i,
                initial_data=saved_data,
                on_update=self._handle_card_update
            )
            self.cards_row.controls.append(card)
            
    def _handle_card_update(self, player_num, key, value):
        print(f"Update detected: Player {player_num} - {key}: {value}")
        
        if player_num not in self.player_states:
            self.player_states[player_num] = {}
            
        self.player_states[player_num][key] = value
        #TODO Hook into OBS Manager and update sources
        prefix = f"P{player_num}"
        
        if key == "name":
            obs_manager.set_source_value(f"{prefix}_Name", value)
        
        elif key == "score":
            obs_manager.set_source_value(f"{prefix}_Score", value)
        
        elif key == "color":
            char_name = self.player_states[player_num].get("character")
            if char_name:
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                abs_path = os.path.join(project_root, "assets", "images", char_name, value)

                obs_manager.set_source_value(f"{prefix}_Character", abs_path)
    
    def _reset_player_data(self, e):
        self.player_states = {}
        count = self.player_count.value
        self._generate_cards(count)
        self.cards_row.update()
        
        