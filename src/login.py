import os
import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../model')))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from flet import (
    Column,
    Container,
    CrossAxisAlignment,
    ElevatedButton,
    MainAxisAlignment,
    Page,
    TextField,
    UserControl,
    colors,
)
from model.customer import Customer
from model.preferences import Preferences

class Login(UserControl):

    def loginClick(self, e):
        self.page.go("/trainingsplan")

    def textChange(self, e):
        self.loginButton.disabled = self.customerIDField.value is None or len(self.customerIDField.value) < 5
        self.setCustomerID(self.customerIDField.value)
        self.update()

    def __init__(self, page, setCustomerID):
        super().__init__()
        prefs = Preferences()
        self.page = page
        self.setCustomerID = setCustomerID
        self.customerID = prefs.customerID
        self.loginButton = ElevatedButton(
            "Login",
            on_click=self.loginClick,
            bgcolor=colors.BLUE,
            color=colors.WHITE,
        )
        self.customerIDField = TextField(
            label="Ihre Kundennummer",
            width=150,
            bgcolor=colors.BLUE_GREY_50,
            border_color=colors.BLUE,
            value=str(self.customerID),
            hint_text="Ihre McFit-Kundennummer",
            on_change=self.textChange,
            data = prefs.customerID
        )
        self.customer = Customer(self.customerIDField.value)
        self.customerIDField.value = self.customerIDField.value
        self.page = page

    def build(self):
        return Container(
                width=500,
                height=300,
                content=Column(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        self.customerIDField,
                        self.loginButton
                    ]
                ),
                bgcolor=colors.WHITE24
            )


#-------------------------- TEST -------------------------#
if __name__ == "__main__":
    c = Login(page=UserControl())
    print(c.customer)
