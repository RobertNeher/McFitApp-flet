from flet import (
    AlertDialog,
    ElevatedButton,
    MainAxisAlignment,
    Text,
    TextButton,
    UserControl,

)

class ConfirmDialog(UserControl):
    def __init__(self, page, title, question, confirmed_action):
        super().__init__()
        self.page = page
        self.action = confirmed_action
        self.title = title
        self.question = question

        self.confirm_dialog = AlertDialog(
            modal=True,
            title=Text(self.title),
            content=Text(self.question),
            actions=[
                TextButton("Ja", on_click=self.action),
                TextButton("Nein", on_click=self.close_dialog),
                TextButton("Abbrechen", on_click=self.close_dialog)
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def close_dialog(self, e):
        self.confirm_dialog.open = False
        self.page.update()

    def open_confirm_dialog(self):
        self.page.dialog = self.confirm_dialog
        self.confirm_dialog.open = True
        self.page.update()

    def build(self):
        self.open_confirm_dialog()
