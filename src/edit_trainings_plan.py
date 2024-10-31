from datetime import datetime
from flet import (
    Column,
    Container,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    Divider,
    Dropdown,
    FontWeight,
    IconButton,
    ListView,
    MainAxisAlignment,
    Row,
    SnackBar,
    Text,
    TextStyle,
    alignment,
    border,
    colors,
    dropdown,
    icons
)
from src.editor import EditPlanMachine
from src.confirm import ConfirmDialog
from src.helper import extract_list, formatDate
from model.machine import Machine
from model.plan import Plan

PARAMETER_ROW_HEIGHT = 20


class EditTrainingsPlan():
    def __init__(self, page, customerID):
        super().__init__()
        self.page = page
        self.customerID = customerID
        self.trainingPlans = Plan(customerID=self.customerID)
        self.dropDownOptions = []
        self.trainingDates = self.trainingPlans.get_valid_from_dates(customerID=self.customerID)
        self.confirmDialog = ConfirmDialog(
            page=self.page,
            title="Bitte bestätige das Löschen",
            question= "Möchtest du den ausgewählten Trainingsplan löschen?",
            confirmed_action=self.delete_record
        )
        self.page.snack_bar = SnackBar(
            content=Text(""),
            bgcolor=colors.RED
        )
        self.planTable = Container()

        if len(self.trainingDates) > 0:
            for plan_date in self.trainingDates:
                date = datetime.strptime(plan_date['valid_from'], "%Y-%m-%d")
                self.dropDownOptions.append(
                    dropdown.Option(datetime.strftime(date, "%d. %B %Y"))
                )

            self.selectedDate = self.dropDownOptions[0].key
            self.planRows = []
            self.parameterCount = 0
        else:
            self.dropDownOptions.append(dropdown.Option("<Keine Daten>"))

        self.planColumns = [
            DataColumn(
                label=Text(
                    "Gerät",
                )
            ),
            DataColumn(
                label=Text(
                    "Parameter",
                )
            ),
            DataColumn(
                label=Text(
                    "Bewegung",
                )
            ),
            DataColumn(
                label=Text(
                    "Hinweise",
                )
            ),
        ]

        self.ParameterTableColumns = [
            DataColumn(
                label=Text(
                    "P",
                )
            ),
            DataColumn(
                numeric=True,
                label=Text(
                    "E",
                )
            ),
        ]

    def handleSelection(self, e):
        EditPlanMachine(page=self.page, fields=e.control.cells)

    def plan_rows(self):
        self.planRows = []

        for machine in self.trainingPlans.get_machines(self.customerID, formatDate(self.selectedDate)):
            self.planRows.append(DataRow(
                cells=[
                    DataCell(
                        content=Text(
                            machine["machine_id"],
                        ),
                    ),
                    DataCell(
                        content=self.ParameterTable(machineID=machine["machine_id"], settings=machine["machine_parameters"]),
                    ),
                    DataCell(
                        content=Text(
                            machine["machine_movement"],
                            size=11,
                        ),
                    ),
                    DataCell(
                        content=Text(
                            machine["machine_comments"],
                            size=11
                        ),
                    )
                ],
                on_select_changed=self.handleSelection
            ))

        return self.planRows

    def ParameterTable(self, machineID, settings):
        machine = Machine(machineID=machineID)
        parameterRows = []
        # parameterView = ListView(padding=0, divider_thickness=0, auto_scroll=True)
        parameterView = Column(
            scroll=True
        )

        parameterNames = extract_list(machine.machines["parameters"])
        parameterValues = extract_list(settings)

        for i in range(0, len(parameterNames)):
            parameterRows.append(
                DataRow(
                    cells=[
                        DataCell(
                            content=Text(parameterNames[i])
                        ),
                        DataCell(
                            content=Text(parameterValues[i])
                        ),
                    ]
                )
            )

        parameterView.controls.append(
            DataTable(
                horizontal_margin=2,
                column_spacing=0,
                heading_row_height=0,
                divider_thickness=0,
                data_row_max_height=PARAMETER_ROW_HEIGHT,
                data_text_style=TextStyle(
                    size = 11,
                    weight = FontWeight.NORMAL,
                    color=colors.BLACK
                ),
                bgcolor=colors.TRANSPARENT,
                sort_column_index=0,
                sort_ascending=True,
                border_radius=0,
                border=None,
                horizontal_lines=None,
                vertical_lines=None,
                rows=parameterRows,
                columns=self.ParameterTableColumns,
            )
        )
        return parameterView

    def setDate(self, e):
        self.selectedDate = e.control.value
        self.page.clean()
        self.page.add(
            self.plan_table(),
        )
        self.page.update()

    def delete_record(self, e):
        self.trainingPlans.deletePlan(ymdDateString=self.selectedDate)
        self.confirmDialog.close_dialog(e)
        self.page.snack_bar.content=Text(
            f"Trainingsplan vom {self.selectedDate} gelöscht!",
            color=colors.WHITE,
            weight=FontWeight.BOLD,
            size=14
        )
        self.page.snack_bar.open = True

    def deletePlan(self, e):
        self.confirmDialog.open_confirm_dialog()

    def newPlan(self, e):
        print("new plan")

    def duplicatePlan(self, e):
        print("duplicate plan")

    def plan_table(self):
        self.planTable = Column(
            scroll=True,
            alignment=MainAxisAlignment.START,
            controls=[

                DataTable(
                    checkbox_horizontal_margin=2,
                    show_checkbox_column=True,
                    bgcolor=colors.WHITE,
                    border_radius=10,
                    horizontal_lines=border.BorderSide(1, colors.BLACK12),
                    sort_column_index=0,
                    sort_ascending=True,
                    heading_text_style=TextStyle(
                        size=16,
                        weight=FontWeight.BOLD,
                        color=colors.BLACK,
                    ),
                    heading_row_color=colors.BLACK12,
                    heading_row_height=50,
                    data_text_style=TextStyle(
                        size=14,
                        weight=FontWeight.NORMAL,
                        color=colors.BLACK,
                    ),
                    divider_thickness=1,
                    column_spacing=30,
                    columns=self.planColumns,
                    rows=self.plan_rows(),
                ),
            ]
        )

        return self.planTable

    def build(self):
        return Column(
            alignment=MainAxisAlignment.START,
            controls=[
                Row(
                    alignment=alignment.center_left,
                    controls=[
                        Text(
                            "Gültig ab",
                            size=16,
                            weight=FontWeight.BOLD,
                            bgcolor=colors.WHITE,
                            color=colors.BLUE,
                        ),
                        Dropdown(
                            value=self.selectedDate,
                            width=190,
                            options=self.dropDownOptions,
                            on_change=self.setDate
                        )
                    ],
                ),
                Divider(
                    color=colors.BLUE,
                    thickness=1,
                ),
                Container(
                    height=50,
                    content=Row(
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                    scroll=True,
                    controls=[
                        IconButton(
                            icon=icons.ADD,
                            on_click=self.newPlan,
                            tooltip="Neuen Plan erstellen",
                        ),
                        IconButton(
                            icon=icons.COPY_ALL,
                            on_click=self.duplicatePlan,
                            tooltip="Aktuellen Plan duplizieren"
                        ),
                        IconButton(
                            icon=icons.DELETE_FOREVER,
                            on_click=self.deletePlan,
                            tooltip="Aktuellen Plan löschen"
                        ),
                    ]
                )),
                Divider(
                    color=colors.BLUE,
                    thickness=1,
                ),
                self.plan_table(),
            ]
        )