from flet import (
    Column,
    CrossAxisAlignment,
    Container,
    ElevatedButton,
    FontWeight,
    MainAxisAlignment,
    Page,
    Text,
    UserControl,
    colors,
)

class About (UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def onClick(self, e):
        self.page.go("/login")
        return

    def build(self):
        okButton = ElevatedButton(
            "OK",
            on_click=self.onClick,
            bgcolor=colors.BLUE,
            color=colors.WHITE,
        )
        aboutText = Text(
            "Deine McFitApp zur Erfassung deiner Trainingsdaten",
            size=24,
            weight=FontWeight.NORMAL,
            width=250,
            bgcolor=colors.WHITE,
            color=colors.BLACK,

        )
        return Container(
                width=500,
                height=300,
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        aboutText,
                        Container(height=20),
                        okButton
                    ]
                ),
                bgcolor=colors.WHITE24
            )
