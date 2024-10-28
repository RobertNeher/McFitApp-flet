import locale

from flet import (
    Page,
    Theme,
    View,
    app,
    colors
)
from src.trainings_overview import TrainingsOverview
from src.about import About
from src.login import Login
from src.trainings_plan import TrainingsPlan
from src.edit_trainings_plan import EditTrainingsPlan
from src.app_bar import mcFitAppBar
from src.edit_preferences import EditPreferences
from model.preferences import Preferences

APP_TITLE = "Dein McFit Trainingsbegleiter"

def main(page: Page):
    customerID = ""
    prefs = Preferences()
    locale.setlocale(locale.LC_TIME, "de_DE")
    page.window_bgcolor = colors,
    page.fonts = {
        "Raleway": "fonts/Raleway-Regular.ttf",
        "McFit": "fonts/McFitApp.ttf",
        "OpenSans": "fonts/OpenSans-Regular.ttf"
    }
    page.theme = Theme(
        color_scheme_seed=colors.BLACK,
        font_family="Raleway",
        use_material3=True
    )
    page.title = APP_TITLE
    page.window_max_height= 1000
    page.window_max_width=500
    page.window_height=1000
    page.window_width=500
    page.route="/trainingsPlanOverview"

    def setCustomerID(e, customer_id):
        customerID = customer_id

    def route_change(route):
        customerID = prefs.customerID

        if page.route == "/login":
            page.views.clear()
            page.views.append(
                View(
                    "/",
                    [
                        mcFitAppBar(page, "Login", "/trainingsplan"),
                        Login(page=page, setCustomerID=setCustomerID)
                    ]
                )
            )

        if page.route == "/trainingsplan":
            page.views.append(
                View(
                    "/trainingsplan",
                    [
                        mcFitAppBar(page, "Dein Trainingsplan", "/login"),
                        TrainingsPlan(page, customerID=customerID)
                    ]
                )
            )

        if page.route == "/editPreferences":
            page.views.append(
                View(
                    "/editPreferences",
                    [
                        mcFitAppBar(page, "Einstellungen", "/login"),
                        EditPreferences(page, "/login")
                    ]
                )
            )

        if page.route == "/trainingsPlanOverview":
            page.views.append(
                View(
                    "/trainingsPlanOverview",
                    [
                        mcFitAppBar(page, "Bearbeitung Trainingspläne", "/login"),
                        EditTrainingsPlan(page, customerID=customerID)
                    ]
                )
            )

        if page.route == "/trainingsOverview":
            page.views.append(
                View(
                    "/trainingsOverview",
                    [
                        mcFitAppBar(page, "Letzte Trainings", "/login"),
                        TrainingsOverview(page, customerID=customerID)
                    ]
                )
            )

        if page.route == "/about":
            page.views.append(
                View(
                    "/about",
                    [
                        mcFitAppBar(page, APP_TITLE, "/login"),
                        About(page)
                    ]
                )
            )
        page.go(page.route)

    def view_pop():
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.update()


app(target=main, assets_dir="./assets")
