import os
import json
import sqlite3 as sl
from datetime import datetime

ASSETS_FOLDER = ".\\assets/\\datasets"
DB_FILE = "assets/mcfit.db"
IMAGE_FOLDER = ".\\assets\\images"
# Table names in local SQLite DB and expected bootstrapping content
PREFERENCE_TABLE = "preferences"
SETTING_TABLE = "settings"
CUSTOMER_TABLE = "customers"
MACHINE_TABLE = "machines"
TRAINING_TABLE = "trainings"
PLAN_TABLE = "plans"
RESULT_TABLE = "results"

class DBConnection:
    def __init__(self, initialize: bool):
        self.connection = sl.connect(DB_FILE, check_same_thread=False)

        with self.connection:
            if initialize:
                self.connection.execute(f"""DROP TABLE IF EXISTS {PREFERENCE_TABLE}
                                        """)
                self.connection.execute(f"""DROP TABLE IF EXISTS {CUSTOMER_TABLE}
                                        """)
                self.connection.execute(f"""DROP TABLE IF EXISTS {MACHINE_TABLE}
                                        """)
                self.connection.execute(f"""DROP TABLE IF EXISTS {PLAN_TABLE}
                                        """)
                self.connection.execute(f"""DROP TABLE IF EXISTS {RESULT_TABLE}
                                        """)

                self.connection.execute(f"""CREATE TABLE {CUSTOMER_TABLE}
                                        (customer_id PRIMARY KEY,
                                        name);
                                        """)
                self.connection.execute(f"""CREATE UNIQUE INDEX CUSTOMER1 ON {CUSTOMER_TABLE}
                                        (customer_id);""")

                self.connection.execute(f"""CREATE TABLE {PREFERENCE_TABLE}
                                        (customer_id REFERENCES {CUSTOMER_TABLE}(customer_id),
                                        duration,
                                        auto_forward);
                                        """)

                self.connection.execute(f"""CREATE TABLE {MACHINE_TABLE}
                                        (name PRIMARY KEY,
                                        title,
                                        description,
                                        parameters,
                                        image blob);
                                        """)
                self.connection.execute(f"""CREATE UNIQUE INDEX MACHINE1 ON {MACHINE_TABLE}
                                        (name);""")

                self.connection.execute(f"""CREATE TABLE {PLAN_TABLE}
                                        (customer_id REFERENCES {CUSTOMER_TABLE}(customer_id),
                                        valid_from,
                                        machine_id REFERENCES {MACHINE_TABLE}(name),
                                        machine_parameters,
                                        machine_movement,
                                        machine_comments);
                                        """)
                self.connection.execute(f"""CREATE UNIQUE INDEX PLAN1 ON {PLAN_TABLE}
                                        (customer_id, valid_from DESC, machine_id);""")
                self.connection.execute(f"""CREATE TABLE {RESULT_TABLE}
                                        (customer_id REFERENCES {CUSTOMER_TABLE}(customer_id),
                                        training_date,
                                        machine_id REFERENCES {MACHINE_TABLE}(name),
                                        duration,
                                        weight_done,
                                        weight_planned);
                                        """)
                self.connection.execute(f"""CREATE UNIQUE INDEX RESULT1 ON {RESULT_TABLE}
                                        (customer_id, training_date, machine_id);""")

                self.connection.commit()

                self.initialize_preferences()
                self.initialize_customers()
                self.initialize_machines()
                self.initialize_plans()
                self.initialize_results()

    def initialize_preferences(self) -> None:
        settings_init_file = os.path.join(ASSETS_FOLDER, PREFERENCE_TABLE + ".json")
        if os.path.isfile(settings_init_file):
            with open(settings_init_file, "r", encoding="UTF-8") as json_file:
                preferences = json.load(json_file)

            for preference in preferences["Preferences"]:
                self.connection.execute(f"""INSERT INTO {PREFERENCE_TABLE} (
                                            customer_id,
                                            studio,
                                            duration,
                                            auto_forward
                                        )
                                        VALUES (
                                            {preference['customer_id']},
                                            {preference['studio']},
                                            {preference['duration']},
                                            {preference['auto_forward']}
                                        )"""
                                )

                self.connection.commit()
                self.preferences = {
                    "customer_id": preference['customer_id'],
                    "studio": preference['studio'],
                    "duration": preference['duration'],
                    "auto_forward": preference['auto_forward']
                }

    def initialize_customers(self) -> None:
        customer_init_file = os.path.join(ASSETS_FOLDER, CUSTOMER_TABLE + ".json")
        if os.path.isfile(customer_init_file):
            with open(customer_init_file, "r", encoding="UTF-8") as json_file:
                customers = json.load(json_file)

            for customer in customers["Customers"]:
                self.connection.execute(f"""INSERT INTO {CUSTOMER_TABLE} (
                                            customer_id,
                                            name
                                        )
                                        VALUES (
                                            {customer['customer_id']},
                                            "{customer['name']}"
                                        )""")

            self.connection.commit()

    def get_customer_name(self, customerID) -> str:
        customers = self.connection.execute(f"""SELECT name FROM {CUSTOMER_TABLE}
                                            WHERE customer_id = {customerID}""")

        result = customers.fetchone()
        return result[0]

    def initialize_machines(self) -> None:
        machine_init_file = os.path.join(ASSETS_FOLDER, MACHINE_TABLE + ".json")
        if os.path.isfile(machine_init_file):
            with open(machine_init_file, "r", encoding="UTF-8") as json_file:
                machines = json.load(json_file)

            for machine in machines["Machines"]:
                with open(f"{IMAGE_FOLDER}\\{machine['name'].strip(' ')}.png", "rb") as image_file:
                    blob_data = image_file.read()

                insert_query = f"""INSERT INTO {MACHINE_TABLE} (
                                            name,
                                            title,
                                            description,
                                            parameters,
                                            image
                                        )
                                        VALUES (
                                         ?, ?, ?, ?, ?
                                        )"""

                data_tuple = (
                    machine['name'],
                    machine['title'],
                    machine['description'],
                    f"{machine['parameters']}",
                    blob_data
                )

                self.connection.execute(insert_query, data_tuple)

            self.connection.commit()

    def initialize_plans(self) -> None:
        plan_init_file = os.path.join(ASSETS_FOLDER, PLAN_TABLE + ".json")
        if os.path.isfile(plan_init_file):
            with open(plan_init_file, "r", encoding="UTF-8") as json_file:
                plans = json.load(json_file)

            for plan in plans["Plans"]:
                for machine in plan["machines"]:
                    self.connection.execute(f"""INSERT INTO {PLAN_TABLE} (
                                                customer_id,
                                                valid_from,
                                                machine_id,
                                                machine_parameters,
                                                machine_movement,
                                                machine_comments
                                            )
                                            VALUES (
                                                "{plan['customer_id']}",
                                                "{plan['valid_from']}",
                                                "{machine['machine_id']}",
                                                "{machine['parameter_values']}",
                                                "{machine['movement']}",
                                                "{machine['comments']}"
                                            )""")

            self.connection.commit()

    def initialize_results(self) -> None:
        result_init_file = os.path.join(ASSETS_FOLDER, RESULT_TABLE + ".json")
        if os.path.isfile(result_init_file):
            with open(result_init_file, "r", encoding="UTF-8") as json_file:
                results = json.load(json_file)

            for result in results["Results"]:
                customer_id = result["customerID"]

                for training in result["trainings"]:
                    training_date = datetime.strptime(training["trainingDate"], "%Y-%m-%d")

                    for result in training["results"]:
                        self.connection.execute(f"""INSERT INTO {RESULT_TABLE} (
                                                    customerID,
                                                    training_date,
                                                    machine_id,
                                                    duration,
                                                    weight_done,
                                                    weight_planned
                                                )
                                                VALUES (
                                                    {customer_id},
                                                    "{training_date.isoformat()}",
                                                    "{result['machineID']}",
                                                    {int(result['duration'])},
                                                    {int(result['doneToday'])},
                                                    {int(result['goalNext'])}
                                                )""")

        self.connection.commit()

    def save_result(self, customerID, training_date, machine_id, duration, weight_done, weight_planned) -> None:
        training_date = datetime.strptime(training_date, "%Y-%m-%d")

        self.connection.execute(f"""INSERT INTO {RESULT_TABLE} (
                                    customer_id,
                                    training_date,
                                    machine_id,
                                    duration,
                                    weight_done,
                                    weight_planned
                                )
                                VALUES (
                                    {customerID},
                                    "{training_date.isoformat()}",
                                    "{machine_id}",
                                    {duration},
                                    {weight_done},
                                    {weight_planned}
                                ON CONFLICT REPLACE
                                )""")



    def __del__(self):
        self.connection.close()


#------------------------ MAIN ------------------------#
if __name__ == "__main__":
    db = DBConnection(initialize=True)
    db.connection.execute(f"""
            DELETE FROM {RESULT_TABLE}
                WHERE training_date LIKE '2023-06-25%'
    """)
    db.connection.commit()

