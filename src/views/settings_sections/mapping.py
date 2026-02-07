import flet as ft
from components.mapping_row import MappingRow
from logic.obs_manager import obs_manager
from logic.config import cfg


class MappingSection(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        self.mapping_rows = []
        connected = obs_manager.ws is not None
        self.obs_options = []
        if connected:
            scenes, inputs = obs_manager.refresh_data()

            self.obs_options = inputs + scenes
        else:
            self.obs_options = ["Not Connected to OBS"]

        self.controls = [
            ft.Text("OBS Source Mapping", size=20, weight="bold"),
            ft.Text("Set your Scenes/Sources", size=12, color="outline"),
            ft.Divider(),
            ft.Divider(),
            ft.Button("Save", icon=ft.Icons.SAVE, on_click=self.save),
        ]

        self.load_initial_data()

    def load_initial_data(self):
        # Load from JSON the Default Settings
        keys_to_render = cfg.get_supported_keys()
        for label in keys_to_render:
            saved_val = cfg.get_mapping(label)
            display_val = saved_val if saved_val else ""
            self.add_row(label, display_val)

    def add_row(self, label, value):
        row = MappingRow(
            label, default_obs_source=value, source_options=self.obs_options
        )
        self.mapping_rows.append(row)
        self.controls.insert(-2, row)

    def did_mount(self):
        self.refresh_all_link_statuses()

    def refresh_all_link_statuses(self):
        for row in self.mapping_rows:
            row.update_link_status()

    def save(self, e):
        final_mapping_dict = {}

        for row in self.mapping_rows:
            data = row.get_data()
            key = data["trigger"]
            value = data["obs_source"]
            final_mapping_dict[key] = value

        cfg.update_mapping(final_mapping_dict)
        print("Saved Mappings:", final_mapping_dict)
