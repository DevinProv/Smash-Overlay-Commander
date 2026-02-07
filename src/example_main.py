import flet as ft

def main(page: ft.Page):
    page.title = "OBS Commander"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#111111"
    page.window_width = 1200
    page.window_height = 900
    
    # --- STYLE CONSTANTS ---
    HEADER_BG = "#1E1E1E"
    MATCH_SETTINGS_BG = "#252525" 
    CARD_BG = "#2D2D2D"
    ACCENT_TEAL = "#00B4D8"
    HOT_DECK_BG = "#1a1a1a"
    
    # --- HELPER: SCORE COUNTER ---
    def create_score_counter():
        return ft.Row([
            ft.IconButton(ft.Icons.REMOVE, icon_color="red", tooltip="-1 Win"),
            ft.Container(
                content=ft.Text("0", size=40, weight="bold", text_align="center"),
                width=60,
                # FIXED: Containers use ft.alignment, not MainAxisAlignment
                alignment=ft.Alignment.CENTER, 
                bgcolor="#111",
                border_radius=5,
                padding=5
            ),
            ft.IconButton(ft.Icons.ADD, icon_color="green", tooltip="+1 Win"),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)

    # --- COMPONENT: MATCH SETTINGS BLOCK (Your New Code) ---
    match_settings_block = ft.Container(
        bgcolor=MATCH_SETTINGS_BG,
        padding=20,
        border_radius=10,
        margin=ft.margin.symmetric(horizontal=40),
        content=ft.Column([
            # Row 1: Match Meta Data
            ft.Row([
                ft.TextField(
                    hint_text="Match Title (e.g. Winners Finals)", 
                    text_size=14, 
                    border_color=ACCENT_TEAL, 
                    expand=True,
                    prefix_icon=ft.Icons.EDIT
                ),
                ft.Dropdown(
                    width=100,
                    options=[
                        ft.dropdown.Option("BO3"),
                        ft.dropdown.Option("BO5"),
                        ft.dropdown.Option("FT10"),
                    ],
                    value="BO3",
                    border_color=ACCENT_TEAL
                )
            ]),
            
            ft.Divider(color="transparent", height=10),
            
            # Row 2: The LIVE Scoreboard
            ft.Container(
                bgcolor="#1a1a1a",
                padding=15,
                border_radius=10,
                content=ft.Row([
                    ft.Text("P1 SCORE", size=12, weight="bold", color="grey"),
                    create_score_counter(), # Left Score
                    
                    ft.Text("-", size=40, weight="bold", color="#555"),
                    
                    create_score_counter(), # Right Score
                    ft.Text("P2 SCORE", size=12, weight="bold", color="grey"),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            )
        ])
    )

    # --- COMPONENT: SIMPLIFIED PLAYER CARD ---
    class PlayerCard(ft.Container):
        def __init__(self, label):
            super().__init__()
            self.bgcolor = CARD_BG
            self.padding = 20
            self.border_radius = 10
            self.expand = True
            self.content = ft.Column([
                ft.Text(label, size=12, color="grey", weight="bold"),
                ft.Row([
                    # Character Icon
                    ft.Container(
                        width=60, height=60, 
                        bgcolor="black", 
                        border_radius=5,
                        border=ft.border.all(1, "#444"),
                        on_click=lambda e: print("Open Char Select")
                    ),
                    # Name Input
                    ft.Column([
                         ft.TextField(
                            hint_text="Player Name", 
                            border_color=ACCENT_TEAL, 
                            height=40, 
                            text_size=16,
                            expand=True,
                            content_padding=10
                        ),
                        ft.TextField(
                            hint_text="Team / Prefix", 
                            border="none", 
                            height=30, 
                            text_size=12,
                            color="grey",
                            content_padding=0
                        ),
                    ], expand=True, spacing=0)
                ]),
            ])

    # --- COMPONENT: HOT DECK REPLAY CARD (Restored) ---
    class ReplayCard(ft.Container):
        def __init__(self, time_label):
            super().__init__()
            self.width = 250
            self.height = 80
            self.bgcolor = "#252525"
            self.border_radius = 8
            self.padding = 10
            self.border = ft.border.all(1, "#333")
            self.content = ft.Row([
                ft.Icon(ft.Icons.PLAY_CIRCLE_FILL, color=ACCENT_TEAL, size=30),
                ft.Column([
                    ft.Text(time_label, size=10, color="grey"),
                    ft.TextField(
                        hint_text="Tag clip...", 
                        text_size=12, 
                        border="none", 
                        height=30,
                        content_padding=0
                    )
                ], spacing=2, expand=True)
            ])

    # --- 1. GLOBAL HEADER (Restored) ---
    header = ft.Container(
        height=70,
        bgcolor=HEADER_BG,
        padding=ft.padding.symmetric(horizontal=20),
        border=ft.border.only(bottom=ft.BorderSide(1, "#333")),
        content=ft.Row([
            ft.Row([
                ft.Icon(ft.Icons.GAMEPAD, color=ACCENT_TEAL),
                ft.Text("SMASH OBS", size=20, weight="bold")
            ]),
            ft.SegmentedButton(
                segments=[
                    ft.Segment(value="caster", label=ft.Text("🎙️ Caster")),
                    ft.Segment(value="game", label=ft.Text("🎮 Game")),
                ],
                selected=["game"], # Use {"game"} (Set) or ["game"] (List) depending on version
            ),
            ft.ElevatedButton(
                "SAVE REPLAY",
                icon=ft.Icons.SAVE,
                bgcolor="red",
                color="white",
                height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                on_click=lambda e: print("BOOM! Replay Saved.")
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    # --- 2. MATCH AREA (Your Layout) ---
    match_area = ft.Container(
        expand=True,
        padding=ft.padding.only(top=20, left=40, right=40),
        content=ft.Column([
            match_settings_block, 
            ft.Divider(height=20, color="transparent"),
            ft.Row([
                PlayerCard("LEFT PLAYER"),
                ft.Text("VS", size=20, color="#333", weight="bold"),
                PlayerCard("RIGHT PLAYER"),
            ], spacing=20)
        ])
    )

    # --- 3. HOT DECK (Restored) ---
    hot_deck = ft.Container(
        height=140,
        bgcolor=HOT_DECK_BG,
        border=ft.border.only(top=ft.BorderSide(1, ACCENT_TEAL)),
        padding=15,
        content=ft.Column([
            ft.Text("RECENT REPLAYS (HOT DECK)", size=10, weight="bold", color=ACCENT_TEAL),
            ft.ListView(
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                horizontal=True,
                spacing=10,
                controls=[
                    ReplayCard("12:42 PM"),
                    ReplayCard("12:30 PM"),
                ]
            )
        ])
    )

    # --- ASSEMBLE LAYOUT ---
    page.add(
        ft.Column([
            header,
            match_area,
            hot_deck
        ], expand=True, spacing=0)
    )

ft.app(target=main)