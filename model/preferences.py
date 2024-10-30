from src import persistence

class Preferences:
    def __init__(self) -> None:
        self.db = persistence.DBConnection(initialize=False)
        pref_row = self.db.connection.execute(f"""SELECT * FROM {persistence.PREFERENCE_TABLE}""")

        result = pref_row.fetchone()

        self.customerID = result[0]
        self.studio = result[1]
        self.duration = int(result[2])
        self.repeats = int(result[3])
        self.auto_forward = result[4] == 1

    def saveSettings(self) -> None:
        self.db.connection.execute(f"""DROP TABLE IF EXISTS {persistence.PREFERENCE_TABLE}""")
        self.db.connection.execute(f"""CREATE TABLE {persistence.PREFERENCE_TABLE}
                                (customer_id REFERENCES {persistence.CUSTOMER_TABLE}(customer_id),
                                studio,
                                duration,
                                repeats,
                                auto_forward);
                                """)
        self.db.connection.commit()

        self.db.connection.execute(f"""INSERT INTO {persistence.PREFERENCE_TABLE} (
                                    customer_id,
                                    studio,
                                    duration,
                                    repeats,
                                    auto_forward
                                )
                                VALUES (
                                    {self.customerID},
                                    {self.studio},
                                    {self.duration},
                                    {self.repeats},
                                    {self.auto_forward}
                                )"""
        )
        self.db.connection.commit()

#-------------------------- TEST -------------------------#
if __name__ == "__main__":
    c = Preferences()
    print(c.auto_forward)
