import flet as ft
from logic.router import Router
from views.dashboard import DashboardView
from views.players import PlayersView
from views.replays import ReplaysView
from components.sidebar import Sidebar
from logic.theme import theme_manager
from logic.obs_manager import obs_manager
from logic.config import cfg


async def main(page: ft.Page):
    page.title = "Smash Desk"
    page.window.width = 1200
    page.window.height = 800
    # Connect to Websocket
    print("Attempting to connect to OBS...")
    obs_manager.connect()

    def on_window_event(e):
        if e.data == "close":
            print("Closing connection to OBS...")
            obs_manager.disconnect()
            page.window_destroy()

    page.window_prevent_close = True
    page.on_window_event = on_window_event

    body_area = ft.Container(expand=True, content=DashboardView())

    my_router = Router(body_area)

    inner_rail = ft.NavigationRail(
        bgcolor=ft.Colors.TRANSPARENT,
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        on_change=lambda e: my_router.go(e.control.selected_index),
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Live"),
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Players"),
            ft.NavigationRailDestination(icon=ft.Icons.VIDEO_LIBRARY, label="Replays"),
        ],
        expand=True,
    )

    def go_to_settings(e):
        inner_rail.selected_index = None
        inner_rail.update()
        my_router.go(99)

    sidebar_wrapper = Sidebar(nav_rail=inner_rail, on_settings_click=go_to_settings)

    page.add(
        ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                sidebar_wrapper,
                ft.VerticalDivider(width=1, color="outline"),
                body_area,
            ],
            expand=True,
        )
    )
    initTheme(page)


def initTheme(page):
    theme = cfg.get_theme()
    saved_theme = theme_manager.get_theme(theme)
    page.theme = saved_theme
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = theme_manager.get_background_color(theme)
    page.update()


ft.run(main)
