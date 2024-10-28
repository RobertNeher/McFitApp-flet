from src import persistence

class Preferences:
    def __init__(self):
        self.db = persistence.DBConnection(initialize=False)
        pref_row = self.db.connection.execute(f"""SELECT * FROM {persistence.PREFERENCE_TABLE}""")

        result = pref_row.fetchone()

        self.customerID = result[0]
        self.duration = int(result[1])
        self.auto_forward = result[2] == 1

    def saveSettings(self):
        self.db.connection.execute(f"""DROP TABLE IF EXISTS {persistence.PREFERENCE_TABLE}""")
        self.db.connection.execute(f"""CREATE TABLE {persistence.PREFERENCE_TABLE}
                                (customer_id REFERENCES {persistence.CUSTOMER_TABLE}(customer_id),
                                duration,
                                auto_forward);
                                """)
        self.db.connection.commit()

        self.db.connection.execute(f"""INSERT INTO {persistence.PREFERENCE_TABLE} (
                                    customer_id,
                                    duration,
                                    auto_forward
                                )
                                VALUES (
                                    {self.customerID},
                                    {self.duration},
                                    {self.auto_forward}
                                )"""
        )
        self.db.connection.commit()

#-------------------------- TEST -------------------------#
if __name__ == "__main__":
    c = Preferences()
    print(c.auto_forward)
