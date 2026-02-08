import flet as ft
from components.mapping_row import MappingRow
from logic.obs_manager import obs_manager
from logic.config import cfg


class MappingSection(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True

        connected = obs_manager.ws is not None
        self.obs_options = []
        if connected:
            scenes, inputs = obs_manager.refresh_data()

            self.obs_options = sorted(inputs + scenes)
        else:
            self.obs_options = ["Not Connected to OBS"]

        self.mapping_rows = []

        self.scrollable_content = ft.Column(
            scroll=ft.ScrollMode.AUTO, expand=True, spacing=10
        )
        self.scroll_container = ft.Container(
            content=self.scrollable_content,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.3, "black"),
            border_radius=10,
            border=ft.Border.all(1, "outlineVariant"),
            padding=15,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.2, "black"),
                blur_style=ft.BlurStyle.INNER,
            ),
        )
        self.footer = ft.Container(
            padding=ft.Padding.only(top=10),
            bgcolor="surface",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.Button(
                        "Save Mappings",
                        icon=ft.Icons.SAVE,
                        on_click=self.save,
                        style=ft.ButtonStyle(
                            bgcolor="primary", color="onPrimary", padding=20
                        ),
                    )
                ],
            ),
        )

        self._build_form()

        self.content = ft.Column(
            controls=[
                ft.Text("OBS Source Mapping", size=24, weight="bold"),
                ft.Text(
                    "Map your App Data to specific OBS Sources",
                    size=14,
                    color="secondary",
                ),
                ft.Divider(height=20, color="transparent"),
                self.scroll_container,
                ft.Divider(height=1, thickness=1),
                self.footer,
            ]
        )

    def _build_form(self):
        keys = cfg.get_supported_keys()

        general_keys = []
        player_buckets = {}

        for k in keys:
            if k.startswith("Player"):
                try:
                    parts = k.split(" ")
                    p_num = int(parts[1])

                    if p_num not in player_buckets:
                        player_buckets[p_num] = []
                    player_buckets[p_num].append(k)
                except:
                    general_keys.append(k)
            else:
                general_keys.append(k)

        self.scrollable_content.controls.append(
            ft.Text("Match Info", weight="bold", size=16)
        )
        gen_container = ft.Container(
            bgcolor="surfaceVariant",
            border_radius=10,
            padding=15,
            content=ft.Column(spacing=15),
        )

        for k in general_keys:
            row = self._create_row(k)
            gen_container.content.controls.append(row)

        self.scrollable_content.controls.append(gen_container)
        self.scrollable_content.controls.append(
            ft.Divider(height=10, color="transparent")
        )

        self.scrollable_content.controls.append(
            ft.Text("Player Sources", weight="bold", size=16)
        )

        for p_num in sorted(player_buckets.keys()):
            p_keys = player_buckets[p_num]

            tile_content = ft.Column(spacing=10)
            for k in p_keys:
                row = self._create_row(k)
                tile_content.controls.append(row)

            player_tile = ft.ExpansionTile(
                title=ft.Text(f"Player {p_num}", weight="bold"),
                subtitle=ft.Text(
                    f"Configure Name, Score, and Character sources for Player {p_num}",
                    size=12,
                ),
                leading=ft.Icon(ft.Icons.PERSON),
                bgcolor="surfaceVariant",
                collapsed_bgcolor="surface",
                controls_padding=15,
                controls=[tile_content],
                expanded=(p_num <= 2),
                shape=ft.RoundedRectangleBorder(radius=8),
                collapsed_shape=ft.RoundedRectangleBorder(radius=8)
            )

            self.scrollable_content.controls.append(player_tile)
            self.scrollable_content.controls.append(ft.Container(height=5))

    def _create_row(self, label):
        saved_val = cfg.get_mapping(label)
        display_val = saved_val if saved_val else ""

        row = MappingRow(
            label, default_obs_source=display_val, source_options=self.obs_options
        )
        self.mapping_rows.append(row)
        return row

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
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text("Mappings Saved!"),
                behavior=ft.SnackBarBehavior.FLOATING,
                elevation=5,
            )
        )
