from flet import (
    AppBar,
    IconButton,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Text,
    TextThemeStyle,
    colors,
    icons,
)

def mcFitAppBar(page:Page, title, backRoute):
    def return2Previous(e):
        page.route=backRoute
        page.update()
    def openEditPreferences(e):
        page.go("/editPreferences")
        page.update()
    def openTrainingsOverview(e):
        page.go("/trainingsOverview")
        page.update()
    def openTrainingsPlanOverview(e):
        page.go("/trainingsPlanOverview")
        page.update()
    def openAbout(e):
        page.go("/about")
        page.update()

    return AppBar(
        leading=IconButton(
            icons.ARROW_BACK, on_click=return2Previous),
        leading_width=40,
        automatically_imply_leading=True,
        title=Text(
            title,
            style=TextThemeStyle(TextThemeStyle.HEADLINE_MEDIUM),
            color=colors.WHITE
        ),
        center_title=False,
        toolbar_height=50,
        bgcolor=colors.BLUE,
        actions=[
            PopupMenuButton(
                items=[
                    PopupMenuItem(
                        text="Einstellungen",
                        on_click=openEditPreferences
                    ),
                    PopupMenuItem(
                        text="Trainingspläne\nbearbeiten",
                        on_click=openTrainingsPlanOverview
                    ),
                    PopupMenuItem(
                        text="Trainings-\nübersicht",
                        on_click=openTrainingsOverview
                    ),
                    PopupMenuItem(
                        text="Über 'McFitApp'",
                        on_click=openAbout
                    ),
                ]
            )
        ] if page.route != "/login" else None
    )
