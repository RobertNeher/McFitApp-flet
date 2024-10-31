import base64
from datetime import datetime

from flet import (
    Column,
    Container,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    Divider,
    FontWeight,
    Image,
    MainAxisAlignment,
    Row,
    Text,
    TextStyle,
    alignment,
    colors,
    icons,
)
from model.machine import Machine
from model.preferences import Preferences
from src.training_results import trainingResults
from model.result import Result

DATE_FORMAT = "%d. %B %Y"

class MachineTabContent():
    def __init__(self,
                 customerID,
                 machineID,
                 parameters,
                 parameterValues,
                 comments,
                 movement,
                 lastResults,
                 lastTab,
                 autoForward):
        super().__init__()
        self.prefs = Preferences()
        self.result = Result(customerID=customerID)
        self.weightPlanned = 0 if (lastResults is None or len(lastResults) == 0) else lastResults["weight_planned"]
        self.duration = self.prefs.duration if (lastResults is None or len(lastResults) == 0) else lastResults["duration"]
        self.weightDone = 0 if (lastResults is None or len(lastResults) == 0) else lastResults["weight_done"]
        self.customerID = customerID
        self.machineID = machineID
        self.machineDetails = Machine(machineID=machineID)
        self.parameters = parameters
        self.parameterValues = parameterValues
        self.comments = comments
        self.movement = movement
        self.lastResults = lastResults
        self.lastTab = lastTab
        self.autoForward = autoForward

        self.paramsHeader = [
            DataColumn(Text("Parameter")),
            DataColumn(Text("Einstellung"))
        ]

        self.paramRows = []

        for i in range(0, len(self.parameters)):
            self.paramRows.append(
                DataRow(
                    cells=[
                        DataCell(Text(self.parameters[i])),
                        DataCell(Text(self.parameterValues[i])),
                    ]
                )
            )

        self.paramTable = DataTable(
            columns=self.paramsHeader,
            rows=self.paramRows,
            column_spacing=10,
            data_text_style=TextStyle(
                color=colors.WHITE,
                weight=FontWeight.NORMAL,
            ),
            divider_thickness=1,
            heading_text_style=TextStyle(
                color=colors.WHITE,
                weight=FontWeight.BOLD,
            ),
            show_bottom_border=False,
        )

    def durationEdit(self, e):
        self.duration = e.control.value

    def weightDoneEdit(self,e):
        self.weightDone = e.control.value

        if self.weightPlanned == "":
            self.weightPlanned = e.control.value

    def weightPlannedEdit(self,e):
        self.duration = e.control.value


    def saveResults(self, duration, weightDone, weightPlanned):
        self.result.saveResults(
            self.machineID,
            duration,
            weightDone,
            weightPlanned
        )

    def build(self):
        stream = base64.b64encode(self.machineDetails.machines["image"]).decode('utf-8')
        return Column(
            alignment=MainAxisAlignment.START,
            tight=True,
            controls=[
                Container(
                    alignment=alignment.top_center,
                    content=Text(
                        f"{self.machineID}-{self.machineDetails.machines['title']}",
                        color=colors.WHITE,
                        size=20,
                        weight=FontWeight.BOLD,
                    )
                ),
                Text(
                    self.machineDetails.machines["description"],
                    color=colors.WHITE,
                    size=14,
                    weight=FontWeight.NORMAL,
                ),
                Divider(thickness=2, height=5,color=colors.BLUE),
                Row(
                    # MainAxisAlignment.START,
                    controls=[
                        Column(
                            alignment=MainAxisAlignment.START,
                            controls=[
                                Text(
                                    "Körperbereiche",
                                    color=colors.WHITE,
                                    size=18,
                                    weight=FontWeight.BOLD
                                ),
                                Image(src_base64=stream,
                                      width=200,
                                      height= 100),
                                self.paramTable,
                            ]
                        ),
                        # TODO: Replacement for non working VerticalDivider control (<0.7.4)
                        Container(
                            height = 350,
                            width = 2,
                            bgcolor=colors.BLUE
                        ),
                        Column(
                            alignment=MainAxisAlignment.END,
                            controls=[
                                Text(
                                    "Bewegung",
                                    color=colors.WHITE,
                                    size=18,
                                    weight=FontWeight.BOLD
                                ),
                                Text(
                                    self.movement,
                                    color=colors.WHITE,
                                    size=14,
                                    weight=FontWeight.NORMAL,
                                    width=175,
                                ),
                                Text(
                                    "Hinweise",
                                    color=colors.WHITE,
                                    size=18,
                                    weight=FontWeight.BOLD
                                ),
                                Text(
                                    self.comments,
                                    color=colors.WHITE,
                                    size=14,
                                    weight=FontWeight.NORMAL,
                                    width=200
                                ),
                            ]
                        ),
                    ]
                ),
                Divider(thickness=2, height=5,color=colors.BLUE),
                Column(
                    alignment=MainAxisAlignment.START,
                    tight=True,
                    controls=[
                        Text(
                            f"Deine Trainingsdaten für heute {datetime.today().strftime(DATE_FORMAT)}",
                            color=colors.WHITE,
                            size=18,
                            weight=FontWeight.BOLD
                        ),
                        Container(height=10),
                        trainingResults(lastResults=self.lastResults,
                                        durationEdit=self.durationEdit,
                                        weightDoneEdit=self.weightDoneEdit,
                                        weightPlannedEdit=self.weightPlannedEdit,
                                        autoForward=self.autoForward,
                                        saveResults=self.saveResults),
                        # Container(height=10),
                        # self.SaveButton(self.lastTab)
                    ]
                )
            ]
        )
