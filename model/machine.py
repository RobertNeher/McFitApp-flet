import src.persistence as persistence

class Machine:
    def __init__(self, machineID):
        self.machineID = machineID
        self.db = persistence.DBConnection(initialize=False)

        machine_rows = self.db.connection.execute(f"""SELECT *
                    FROM {persistence.MACHINE_TABLE}
                    {f"WHERE name = '{machineID}'" if machineID is not None else ""}
                    """)
        result = [dict((machine_rows.description[i][0], value)
               for i, value in enumerate(row)) for row in machine_rows.fetchall()]

        if machineID is None:
            self.machines = (result if len(result) > 0 else None)
        else:
            self.machines = result[0]

#-------------------------- TEST -------------------------#
if __name__ == "__main__":
    m = Machine("D5")
