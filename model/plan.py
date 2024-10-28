import src.persistence as persistence

class Plan:
    def __init__(self, customerID):
        self.customerID = customerID
        self.db = persistence.DBConnection(initialize=False)
        self.latestPlan = self.get_valid_from_dates(customerID=self.customerID)[0]

    # def machine_parameter_values(self, machineID):
    #     customer_machines =  self.machines
    #     if customer_machines is not None:
    #         for machine in self.plan:
    #             if machine["machineID"] == machineID:
    #                 return machine["parameterValues"]

    #     return None

    def get_machines(self, customerID, ymdDate):
        machine_rows = self.db.connection.execute(f"""SELECT machine_id, machine_parameters, machine_movement, machine_comments
                FROM {persistence.PLAN_TABLE} WHERE customer_id="{customerID}"
                AND valid_from LIKE '{ymdDate}%'
                """)
        result = [dict((machine_rows.description[i][0], value)
               for i, value in enumerate(row)) for row in machine_rows.fetchall()]

        return (result if len(result) > 0 else None)

    def get_valid_from_dates(self, customerID):
        dates = self.db.connection.execute(f"""SELECT DISTINCT valid_from
                    FROM {persistence.PLAN_TABLE} WHERE customer_id="{customerID}"
                    ORDER BY valid_from DESC
                    """)
        result = [dict((dates.description[i][0], value)
               for i, value in enumerate(row)) for row in dates.fetchall()]

        return (result if len(result) > 0 else None)


    def deletePlan(self, ymdDateString):
        SQLCommand = f"DELETE FROM {persistence.PLAN_TABLE}"

        if ymdDateString != "Alle":
            SQLCommand += f" WHERE valid_from LIKE '{ymdDateString}%'"

        self.db.connection.execute(SQLCommand)
        self.db.connection.commit()


#-------------------------- TEST -------------------------#
if __name__ == "__main__":
    p = Plan(customerID="TÜ001-6876582")
    print(p.latestPlan)
    print(p.get_machines(customerID="TÜ001-6876582", ymdDate="2024-10-27"))
