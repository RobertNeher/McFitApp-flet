from flet import (
    Page,
    app,
)
from src.edit_trainings_plan import EditTrainingsPlan


def main(page: Page):
    page.add(EditTrainingsPlan(customerID="19711", page=page))

if __name__ == "__main__":
    app(target=main)