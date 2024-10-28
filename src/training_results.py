from flet import (
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    InputBorder,
    Text,
    TextField,
    colors,
)

from model.preferences import Preferences

def trainingResults(lastResults, durationEdit, weightDoneEdit, weightPlannedEdit, autoForward, saveResults):

    def copyValue(e):
        if (weightPlannedField.value) == '' or int(weightPlannedField.value) == 0:
            weightPlannedField.value = e.control.value
            weightPlannedField.update()

    def onSubmit(e):
        # saveResults()
        saveResults(durationField.value, weightDoneField.value, weightPlannedField.value)

    prefs = Preferences()

    durationField=TextField(
        color=colors.WHITE,
        border=InputBorder.UNDERLINE,
        border_color=colors.WHITE,
        focused_color=colors.WHITE,
        on_change=durationEdit,
        width=150,
        value=prefs.duration if (lastResults is None or len(lastResults) == 0) else str(lastResults["duration"])
    )
    weightDoneField=TextField(
        color=colors.WHITE,
        border=InputBorder.UNDERLINE,
        border_color=colors.WHITE,
        focused_color=colors.WHITE,
        autofocus=True,
        on_change=weightDoneEdit,
        on_blur=copyValue,
        width=150,
        value="0" if (lastResults is None or len(lastResults) == 0) else str(lastResults["weight_done"])
    )

    weightPlannedField=TextField(
        color=colors.WHITE,
        border=InputBorder.UNDERLINE,
        border_color=colors.WHITE,
        focused_color=colors.WHITE,
        on_blur=autoForward,
        on_change=weightPlannedEdit,
        on_submit=onSubmit,
        width=150,
        value="0" if (lastResults is None or len(lastResults) == 0) else str(lastResults["weight_planned"])
    )

    resultsColumns = [
        DataColumn(
            label=Text(
                "1",
                height=0,
            )
        ),
        DataColumn(
            label=Text(
                "2",
                height=0,
                width=150,
            )
        ),
        DataColumn(
            label=Text(
                "3",
                height=0
            )
        ),
    ]
    resultsRows = [
        DataRow(
            cells=[
                DataCell(
                    content=Text(
                        "Dauer:",
                        size=14,
                        color=colors.WHITE
                    ),
                ),
                DataCell(
                    content=durationField
                ),
                DataCell(
                    content=Text(
                        "sec.",
                        size=14,
                        color=colors.WHITE
                    ),
                ),
            ]
        ),
        DataRow(
            cells=[
                DataCell(
                    content=Text(
                        "heute aufgelegt:",
                        size=14,
                        color=colors.WHITE
                    ),
                ),
                DataCell(
                    content=weightDoneField
                ),
                DataCell(
                    content=Text(
                        "lbs.",
                        size=14,
                        color=colors.WHITE
                    ),
                ),
            ]
        ),
        DataRow(
            cells=[
                DataCell(
                    content=Text(
                        "Auflage für\ndas nächste Mal:",
                        size=14,
                        color=colors.WHITE
                    ),
                ),
                DataCell(
                    content=weightPlannedField
                ),
                DataCell(
                    content=Text(
                        "lbs.",
                        size=14,
                        color=colors.WHITE
                    ),
                ),
            ]
        ),

    ]
    return DataTable(
            bgcolor=colors.BLACK,
            columns=resultsColumns,
            heading_row_height=0,
            rows=resultsRows,
            column_spacing=10,
            divider_thickness=0,
            data_row_color=colors.BLUE_GREY,
            show_bottom_border=False,
        )
