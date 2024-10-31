from datetime import datetime
from flet import (
    Container,
    Column,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    Divider,
    Dropdown,
    IconButton,
    FontWeight,
    MainAxisAlignment,
    OutlinedButton,
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
from src.helper import formatDate
from src.confirm import ConfirmDialog
from model.result import Result

class TrainingsOverview():
    def __init__(self, page, customerID):
        super().__init__()
        self.page = page
        self.customerID = customerID
        self.results = Result(customerID=self.customerID)
        self.dropDownOptions = []
        self.trainingDates = self.results.trainingdates(latest=False)
        self.confirmDialog = ConfirmDialog(
            page=self.page,
            title="Bitte bestätige das Löschen",
            question= "Möchtest du das ausgewählte Trainingsresultat löschen?",
            confirmed_action=self.delete_record
        )
        self.page.snack_bar = SnackBar(
            content=Text(""),
            bgcolor=colors.RED
        )

        if len(self.trainingDates) > 0:
            for trainingDate in self.trainingDates:
                date = datetime.strptime(trainingDate['training_date'], "%Y-%m-%d")
                self.dropDownOptions.append(
                    dropdown.Option(datetime.strftime(date, "%d. %B %Y"))
                )

            self.selectedDate = self.dropDownOptions[0].key
            self.resultRows = []
        else:
            self.dropDownOptions.append(dropdown.Option("<Keine Daten>"))

        self.resultColumns = [
            DataColumn(
                label=Text(
                    "Gerät",
                )
            ),
            DataColumn(
                numeric=True,
                label=Text(
                    "Dauer",
                )
            ),
            DataColumn(
                numeric=True,
                label=Text(
                    "aufgelegtes\nGewicht",
                )
            ),
            DataColumn(
                numeric=True,
                label=Text(
                    "geplantes\nGewicht",
                )
            ),
        ]

    def result_rows(self, trainingsDate):
        self.resultRows = []
        trainingData = self.results.byDate(trainingDate=formatDate(dateString=trainingsDate))

        for machine in trainingData:
            self.resultRows.append(DataRow(
                cells=[
                    DataCell(
                        content=Text(
                            machine["machine_id"],
                        ),
                    ),
                    DataCell(
                        content=Text(
                            machine["duration"],
                        ),
                    ),
                    DataCell(
                        content=Text(
                            machine["weight_done"],
                        ),
                    ),
                    DataCell(
                        content=Text(
                            machine["weight_planned"],
                        ),
                    )
                ]
            ))

        return self.resultRows

    def setDate(self, e):
        self.selectedDate = e.control.value
        self.resultTable = self.result_table()
        self.page.clean()
        self.page.add(
            self.result_table(),
        )
        self.page.update()

    def delete_record(self, e):
        self.results.deleteResults(self.formatDate(self.selectedDate))
        self.confirmDialog.close_dialog(e)
        self.page.snack_bar.content=Text(
            f"Trainingsresultate vom {self.selectedDate} gelöscht!",
            color=colors.WHITE,
            weight=FontWeight.BOLD,
            size=14
        )
        self.page.snack_bar.open = True

    def deleteResults(self, e):
        self.confirmDialog.open_confirm_dialog()

    def result_table(self):
        self.resultRows = self.result_rows(self.selectedDate)
        self.resultTable = Column(
                alignment=MainAxisAlignment.START,
                controls=[
                    Row(
                        alignment=alignment.center_left,
                        controls=[
                            Text(
                                "Trainingsdatum",
                                size=16,
                                weight=FontWeight.BOLD,
                                bgcolor=colors.WHITE,
                                color=colors.BLUE,
                            ),
                            Dropdown(
                                value=self.selectedDate,
                                width=170,
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
                                icon=icons.DELETE_FOREVER,
                                on_click=self.deleteResults,
                                tooltip="Aktuelles Trainingsreultat löschen"
                            ),
                        ]
                    )),
                    Divider(
                        color=colors.BLUE,
                        thickness=1,
                    ),

                    DataTable(
                        bgcolor=colors.WHITE,
                        border_radius=10,
                        vertical_lines=border.BorderSide(1, colors.BLACK12),
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
                        data_row_height=40,
                        data_text_style=TextStyle(
                            size=14,
                            weight=FontWeight.NORMAL,
                            color=colors.BLACK,
                        ),
                        divider_thickness=1,
                        column_spacing=30,
                        columns=self.resultColumns,
                        rows=self.resultRows,
                    ),
                ]
            )

        return self.resultTable

    def build(self):
        return self.result_table()