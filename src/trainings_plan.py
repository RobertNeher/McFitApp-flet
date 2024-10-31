from flet import (
    Container,
    FontWeight,
    Page,
    Tab,
    Tabs,
    Text,
    alignment,
    colors,
)
from model.preferences import Preferences
from model.machine import Machine
from model.plan import Plan
from model.result import Result
from src.machine_tab_content import MachineTabContent
from src.helper import extract_list

class TrainingsPlan():
    def __init__(self, page, customerID):
        super().__init__()
        self.customerID = customerID
        self.machineTabs = []
        self.plan = Plan(customerID=customerID)
        self.results = Result(customerID=customerID)
        self.page = page
        self.prefs = Preferences()
        self.tabs = []

    def saveResults(self, e):
        for machineTab in self.machineTabs:
            print(machineTab.weightPlannedEdit)

    def triggerAutoForward(self, e):
        if self.prefs.auto_forward:
            self.tabs.index += 1 if self.tabs.index < len(self.plan) - 1 else 0

    def build(self):
        i = 0
        planDates = self.plan.get_valid_from_dates(customerID=self.customerID)

        if len(planDates) > 0:
            self.latestPlan = self.plan.get_machines(customerID=self.customerID, ymdDate=planDates[0]["valid_from"])
        else:
            self.latestPlan = None

        for machine in self.latestPlan:
            machineDetail = Machine(machineID=machine["machine_id"])

            parameters = extract_list(machineDetail.machines["parameters"])
            values = extract_list(machine["machine_parameters"])

            self.machineTabs.append(Tab(
                tab_content=Container(
                        alignment=alignment.center,
                        height=40,
                        # width=45,
                        bgcolor=colors.BLUE,
                        content=Text(machine["machine_id"],
                            size=24,
                            weight=FontWeight.BOLD,
                            color=colors.WHITE
                        ),
                ),
                content=Container(
                    padding=10,
                    bgcolor=colors.BLACK,
                    content=MachineTabContent(
                        customerID = self.customerID,
                        machineID=machine["machine_id"],
                        parameters=parameters,
                        parameterValues=values,
                        comments=machine["machine_comments"],
                        movement=machine["machine_movement"],
                        lastResults=self.results.latest(machineID=machine["machine_id"]),
                        lastTab=(i == (len(self.latestPlan) - 1)),
                        autoForward=self.triggerAutoForward)
                    ),
                )
            )
            i += 1

        return Container(
            height=900,
            padding=0,
            content=Tabs(
                selected_index=0,
                tabs=self.machineTabs,
                indicator_color=colors.RED,
                indicator_tab_size=True,
                indicator_border_radius=5,
                indicator_padding=3,
                indicator_border_side=colors.AMBER,
                divider_color=colors.BLACK
            )

        )


#-------------------------- TEST -------------------------#
# if __name__ == "__main__":
#     plan = TrainingsPlan(page=Page(), customerID=19711)

#     print(plan.machines)
#     print(plan.plan)