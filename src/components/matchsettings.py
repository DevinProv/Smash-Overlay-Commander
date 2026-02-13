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

        self.current_drag_src = None
        self.player_states = {}

        min_p = cfg.data.get("min_players", 2)
        max_p = cfg.data.get("max_players", 4)
        self.player_count = CounterInput(
            value=2,
            min_value=min_p,
            max_value=max_p,
            text_size=18,
            on_change=self._on_player_count_change,
        )
        print(cfg.get_mapping("Match Title"))
        self.match_title = ft.TextField(
            hint_text="e.g. Winners Finals",
            border_radius=8,
            content_padding=12,
            text_size=14,
            height=45,
            expand=True,
            on_change=lambda e: self._update_match_title(),
        )
        self.reset_btn = ft.IconButton(
            ft.Icons.REFRESH,
            icon_color=ft.Colors.RED_800,
            tooltip="Reset Player Data",
            on_click=self._reset_player_data,
        )
        self.cards_row = ft.Row(
            wrap=True,
            spacing=30,
            run_spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            run_alignment=ft.MainAxisAlignment.CENTER,
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
                    controls=[
                        ft.Text(
                            "Player Controls", size=14, color="outline", weight="bold"
                        ),
                        self.reset_btn,
                    ]
                ),
                ft.Container(
                    expand=True, alignment=ft.Alignment.CENTER, content=self.cards_row
                ),
            ],
        )
    
    def _set_drag_source(self, i):
        self.current_drag_src = i
    
    
    def _update_match_title(self):
        title = self.match_title.value
        obs_source = cfg.get_mapping("Round Title")
        if obs_source:
            try:
                obs_manager.set_source_value(obs_source, title)
            except Exception as e:
                print(f"Error updating OBS source for Round Title: {e}")

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
        self.player_cards = []

        for i in range(1, count + 1):
            saved_data = self.player_states.get(i, {})
            drag_handle = ft.Draggable(
                group="player_swap",
                data=str(i),
                content=ft.Icon(
                    ft.Icons.DRAG_INDICATOR, color="white54", tooltip="Drag to Swap"
                ),
                content_when_dragging=ft.Container(
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.BLUE_GREY_700,
                    border_radius=5,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.SWAP_HORIZ, color="white"),
                    opacity=0.9
                ),
                on_drag_start=lambda e, idx=i: self._set_drag_source(idx),
            )
            card = PlayerCard(
                player_num=i,
                initial_data=saved_data,
                on_update=self._handle_card_update,
                drag_handle=drag_handle,
            )
            self.player_cards.append(card)

            drag_target = ft.DragTarget(
                group="player_swap",
                content=card,
                on_accept=self._on_card_drop,
                on_will_accept=self._on_drag_enter,
                on_leave=self._on_drag_leave,
                data=str(i),
            )

            self.cards_row.controls.append(drag_target)

    def _on_card_drop(self, e):
        try:
            src_index = self.current_drag_src
            dest_str = e.control.data
            
            if src_index is None:
                print("No source index set for drag operation.")
                return
            
            dest_index = int(dest_str)

            if src_index == dest_index:
                print("Source and destination are the same, no swap needed.")
                return
            self._swap_players(src_index, dest_index)
            self._on_drag_leave(e)
            
        except Exception as e:
            print(f"Error handling card drop: {e}")


    def _swap_players(self, p1_idx, p2_idx):
        idx1 = p1_idx - 1
        idx2 = p2_idx - 1

        card1 = self.player_cards[idx1]
        card2 = self.player_cards[idx2]

        data1 = card1.get_data()
        data2 = card2.get_data()
        card1.set_data(data2)
        card2.set_data(data1)

        self.page.show_dialog(
            ft.SnackBar(ft.Text(f"Swapped Player {p1_idx} and Player {p2_idx}"))
        )

    def _handle_card_update(self, player_num, key, value):
        print(f"Update detected: Player {player_num} - {key}: {value}")

        if player_num not in self.player_states:
            self.player_states[player_num] = {}

        self.player_states[player_num][key] = value
        # TODO Hook into OBS Manager and update sources
        new_key = (
            f"Player {player_num} Character"
            if key == "color"
            else f"Player {player_num} {key.capitalize()}"
        )
        if "character" in key.lower():
            new_value = "default.png"
        else:
            new_value = value

        print(f"Looking for mapping with key: '{new_key}'")

        source = cfg.get_mapping(f"{new_key}")
        char_name = self.player_states[player_num].get("character")

        try:
            if source:
                if "character" in new_key.lower() and char_name:
                    self._update_char_image_source(player_num, char_name, new_value)
                else:
                    obs_manager.set_source_value(source, new_value)
            else:
                print(f"No OBS source mapped for Player {player_num} {key}")
        except Exception as e:
            print(f"Error updating OBS source for Player {player_num} {key}: {e}")

    def _on_drag_start(self, e):
        self.current_drag_src = e.control.data
        pass

    def _on_drag_enter(self, e):
        card = e.control.content
        card.border = ft.Border.all(2, "yellow")
        card.scale = 0.95
        card.shadow = ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.with_opacity(0.5, ft.Colors.CYAN_400)
        )
        card.update()

    def _on_drag_leave(self, e):
        card = e.control.content
        card.scale = 1.0
        card.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.2, "black"),
            offset=ft.Offset(0, 5),
        )
        color = card.color_dropdown.value
        card._update_card_border(color)

    def _reset_player_data(self, e):
        self.player_states = {}
        count = self.player_count.value
        self._generate_cards(count)
        self.cards_row.update()

    def _update_char_image_source(self, player_num, char_name, image_file):
        source = cfg.get_mapping(f"Player {player_num} Character")
        if not source:
            print(f"No OBS source mapped for Player {player_num} Character")
            return

        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        abs_path = os.path.join(project_root, "assets", "images", char_name, image_file)

        try:
            obs_manager.set_source_value(source, abs_path)
            print(
                f"Updated character image source for Player {player_num} to {abs_path}"
            )
        except Exception as e:
            print(f"Error updating character image source for Player {player_num}: {e}")
