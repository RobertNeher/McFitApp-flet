from datetime import datetime
from flet import (
    AlertDialog,
    Dropdown,
    MainAxisAlignment,
    Row,
    SnackBar,
    Text,
    TextButton,
    TextField,
    UserControl,
    dropdown,
)
from src.helper import extract_list, formatDate
from model.machine import Machine

class EditPlanMachine(UserControl):
    def __init__(self, page, fields):
        super().__init__()
        self.fields = fields
        self.allMachines = Machine(machineID=None)
        self.page = page
        self.machine = ""
        self.parameters = []
        self.movement = ""
        self.comment = ""
        self.title = "Änderung"
        self.machinesDropDownOptions = []

        for machine in self.allMachines.machines:
            self.machinesDropDownOptions.append(dropdown.Option(machine["name"]))

        def setMachine(self, e):
            self.machine = e.control.value

        self.machinesDropDown = Dropdown(
            autofocus=True,
            label="Geräte",
            width=100,
            value=self.fields[0].content.value,
            options=self.machinesDropDownOptions,
            on_change=self.setMachine,
        )

        def handleParameter(self, e):
            print(e.control.data)
    
        self.parameterEdit = TextField(
            label="Parameters",
            disabled=True,
            value=self.fields[1].content.value,
            width=150,
        )

        def setMovement(self, e):
            self.movement = e.control.value
    
        self.movementEdit = TextField(
            label="Bewegung",
            value=self.fields[2].content.value,
            width=150,
            on_change=self.setMovement,
        )

        def setComment(self, e):
            self.comment = e.control.value
    
        self.commentEdit = TextField(
            label="Hinweise",
            value=self.fields[3].content.value,
            width=150,
            on_change=self.setComment
        ),


        self.edit_dialog = AlertDialog(
            modal=True,
            title=Text(self.title),
            content=Row(
                controls=[
                    self.machinesDropDown,
                    self.parameterEdit,
                    self.movementEdit,
                    self.commentEdit,
                ]
            ),
            actions=[
                TextButton("Speichern", on_click=self.savePlanEntry),
                TextButton("Verwerfen", on_click=self.close_dialog),
                TextButton("Abbrechen", on_click=self.close_dialog)
            ],
            actions_alignment=MainAxisAlignment.START,
        )

    def close_dialog(self, e):
        self.edit_dialog.open = False
        self.page.update()

    def open_confirm_dialog(self, e):
        self.page.dialog = self.confirm_dialog
        self.edit_dialog.open = True
        self.page.update()

    def savePlanEntry(self, e):
        print(f"Save {self.machinesDropDown.value}")

    def build(self):
        self.open_confirm_dialog()
