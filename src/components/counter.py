import flet as ft


class CounterInput(ft.Row):
    def __init__(self, value=2, min_value=2, max_value=99, on_change=None, text_size=20):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.on_change = on_change
        
        self.alignment = ft.MainAxisAlignment.CENTER
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10
        self.width = 160
        
        self.text_display = ft.Text(
            str(self.value),
            size=text_size,
            weight="bold",
            text_align="center",
            width=50,
            font_family="Monospace"
        )
        
        self.btn_minus = self._create_button(ft.Icons.REMOVE, self._decrement)
        self.btn_plus = self._create_button(ft.Icons.ADD, self._increment)
        
        self.controls = [
                self.btn_minus,
                self.text_display,
                self.btn_plus
            ]
        
    def _create_button(self, icon, func):
        return ft.Container(
            content=ft.Icon(icon, size=16, color="onPrimary"),
            width=32,
            height=32,
            bgcolor="primary",
            border_radius=16,
            on_click=func,
            ink=True,
            alignment=ft.Alignment.CENTER,
            shadow=ft.BoxShadow(
                blur_radius=5,
                color=ft.Colors.with_opacity(0.3, "black"),
                offset=ft.Offset(0, 2)
                )
        )
    
    def _decrement(self, e):
        if self.value > self.min_value:
            self.value -= 1
            self._update_display()
    
    def _increment(self,e):
        if self.value < self.max_value:
            self.value += 1
            self._update_display()
    
    def _update_display(self):
        self.text_display.value = str(self.value)
        self.text_display.update()
        if self.on_change:
            self.on_change(self.value)
    
    def get_value(self):
        return self.value
    