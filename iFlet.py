import flet as ft

def main(page: ft.Page):

    def get_code(e):
        lines = [line for line in tb2.value.split('\n') if line.strip()]
        print(lines)

    tb2 = ft.TextField(
        label="Auto adjusted height with max lines",
        multiline=True,
        min_lines=15,
        max_lines=300,
    )
    
    b = ft.ElevatedButton(text="Execute", on_click=get_code)

    page.add(tb2, b)

ft.app(target=main)
