from flet import (
    Checkbox,
    Column,
    CrossAxisAlignment,
    Container,
    Divider,
    ElevatedButton,
    FontWeight,
    InputBorder,
    MainAxisAlignment,
    Page,
    Row,
    Text,
    TextField,
    UserControl,
    alignment,
    colors,
)

from model.preferences import Preferences

class EditPreferences(UserControl):
    def __init__(self, page: Page, backRoute):
        super().__init__()
        self.prefs=Preferences()
        self.page = page
        self.backRoute = backRoute

        self.durationField=TextField(
            color=colors.BLACK,
            border=InputBorder.UNDERLINE,
            border_color=colors.WHITE,
            focused_color=colors.BLUE,
            on_change=self.durationEdit,
            width=150,
            value=self.prefs.duration
        )
        self.autoForwardField=Checkbox(
            on_change=self.autoForwardEdit,
            width=150,
            value=self.prefs.auto_forward == 1
        )
        self.customerIDField=TextField(
            color=colors.BLACK,
            border=InputBorder.UNDERLINE,
            border_color=colors.WHITE,
            focused_color=colors.BLUE,
            on_change=self.customerIDEdit,
            width=150,
            value=self.prefs.customerID
        )

    def routeBack(self, e):
        self.page.go(self.backRoute)
        return

    def durationEdit(self, e):
        self.prefs.duration = e.control.value

    def autoForwardEdit(self, e):
        self.prefs.auto_forward = 1 if e.control.value else 0

    def customerIDEdit(self, e):
        self.prefs.customerID = e.control.value

    def saveSettings(self, e):
        self.prefs.saveSettings()
        self.page.go(self.backRoute)

    def build(self):
        return Container(
                width=500,
                height=300,
                bgcolor=colors.WHITE,
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Row(
                            alignment=alignment.top_center,
                            controls=[
                                Text(
                                    "Standarddauer",
                                    size=18,
                                    weight=FontWeight.NORMAL,
                                    width=250,
                                    bgcolor=colors.WHITE,
                                    color=colors.BLACK,
                                ),
                                self.durationField,
                                Text(
                                    "sec.",
                                    size=18,
                                    weight=FontWeight.NORMAL,
                                    width=250,
                                    bgcolor=colors.WHITE,
                                    color=colors.BLACK,
                                )
                            ]
                        ),
                        Divider(
                            color=colors.BLUE,
                            thickness=2,
                        ),
                        Row(
                            alignment=alignment.center_left,
                            controls=[
                                Text(
                                "Automatisches\nWeiterschalten\nauf nächstes Gerät",
                                    size=18,
                                    weight=FontWeight.NORMAL,
                                    width=250,
                                    bgcolor=colors.WHITE,
                                    color=colors.BLACK,
                                ),
                                self.autoForwardField,
                                Text(
                                    "",
                                    size=18,
                                    weight=FontWeight.NORMAL,
                                    width=250,
                                    bgcolor=colors.WHITE,
                                    color=colors.BLACK,
                                )
                            ]
                        ),
                        Divider(
                            color=colors.BLUE,
                            thickness=2,
                        ),
                        Row(
                            alignment=alignment.center_left,
                            controls=[
                                Text(
                                    "Ihre Kundennummer",
                                    size=18,
                                    weight=FontWeight.NORMAL,
                                    width=250,
                                    bgcolor=colors.WHITE,
                                    color=colors.BLACK,
                                ),
                                self.customerIDField,
                                Text(
                                    "",
                                    size=18,
                                    weight=FontWeight.NORMAL,
                                    width=250,
                                    bgcolor=colors.WHITE,
                                    color=colors.BLACK,
                                )
                            ]
                        ),
                        Container(
                            height=10
                        ),
                        ElevatedButton(
                            "Speichern",
                            on_click=self.saveSettings,
                            bgcolor=colors.BLUE,
                            color=colors.WHITE,
                        )
                    ]
                ),
            )
