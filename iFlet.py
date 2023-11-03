import flet as ft


class TextEditor(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.on_keyboard_event = self.on_tab_press

    def on_tab_press(self, event: ft.KeyboardEvent):
            if event.key == 'tab':
                event.widget.insert('insert','\t')
                return 'break'

    def build(self):
            
        self.main_tf = ft.TextField(
            label="Let's Code Membranes",
            multiline=True, 
            autofocus=True,
            border=ft.InputBorder.NONE
        )
        return self.main_tf

def main(page: ft.Page):

    def get_code(e):
        lines = [line for line in text.value.split('\n') if line.strip()]
        print(lines)

    page.scroll = ft.ScrollMode.ALWAYS
    text = TextEditor(page)

    b = ft.ElevatedButton(text="Execute", on_click=get_code)

    page.add(text, b)

ft.app(target=main)
