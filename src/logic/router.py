from views.dashboard import DashboardView
from views.players import PlayersView
from views.replays import ReplaysView
from views.settings import SettingsView


class Router:
    def __init__(self, body_container):
        self.body = body_container
        self.routes = {
            0: DashboardView,
            1: PlayersView,
            2: ReplaysView,
            99: SettingsView,
        }
        self.cache = {}

    def go(self, index):
        if index not in self.cache:
            self.cache[index] = self.routes[index]()

        self.body.content = self.cache[index]
        self.body.update()
