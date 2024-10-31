import os
from datetime import datetime
import src.persistence

class Result:
    def __init__(self, customerID):
        self.customerID = customerID
        self.timeStamp = datetime.today().strftime("%Y-%m-%d")

        self.db = src.persistence.DBConnection(initialize=False)
        self.cursor = self.db.connection.cursor()

    def all(self):
        SQL = f"""SELECT *
                    FROM {src.persistence.RESULT_TABLE}
                    WHERE customer_id = ?
                    """
        result_rows = self.cursor.execute(SQL, [self.customerID])

        result = [dict((result_rows.description[i][0], value)
               for i, value in enumerate(row)) for row in result_rows.fetchall()]

        return (result if len(result) > 0 else None)

    def trainingdates(self, latest: bool):
        SQL = f"""SELECT DISTINCT training_date
                    FROM {src.persistence.RESULT_TABLE}
                    WHERE customer_id = ?
                    ORDER BY training_date DESC
                    """
        result_rows = self.cursor.execute(SQL, [self.customerID])

        result = [dict((result_rows.description[i][0], value[0:10])
               for i, value in enumerate(row)) for row in result_rows.fetchall()]

        if len(result) > 0:
            return (result[0] if latest else result)
        else:
            return None

    def byDate(self, trainingDate):
        SQL = f"""SELECT
                    machine_id,
                    duration,
                    weight_done,
                    weight_planned
                    FROM {src.persistence.RESULT_TABLE}
                    WHERE customer_id = ?
                    AND training_date LIKE '?%'
                    ORDER BY machine_id
                    """
        result_rows = self.cursor.execute(SQL, [self.customerID, trainingDate[0:10]])

        result = [dict((result_rows.description[i][0], value)
               for i, value in enumerate(row)) for row in result_rows.fetchall()]

        if len(result) > 0:
            return result
        else:
            return None

    def latest(self, machineID):
        latestDate =  self.trainingdates(latest=True)

        if latestDate is None:
            latest_training = ""
        else:
            latest_training = latestDate["training_date"]

        if machineID is None:
            SQL = f"""SELECT *
                        FROM {src.persistence.RESULT_TABLE}
                        WHERE customer_id = ? AND training_date = '?'
                        ORDER BY machine_id
                        """
            result_rows = self.cursor.execute(SQL, [self.customerID, latest_training])
        else:
            SQL = f"""SELECT *
                        FROM {src.persistence.RESULT_TABLE}
                        WHERE customer_id = ?"""
            SQL += "AND training_date LIKE '?%'" if len(latest_training) > 0 else ""
            SQL += " AND machine_id = ?"

        if len(latest_training) == 0:
            result_rows = self.cursor.execute(SQL, [self.customerID, machineID])
        else:
            result_rows = self.cursor.execute(SQL, [self.customerID, latest_training, machineID])

        result = [dict((result_rows.description[i][0], value)
               for i, value in enumerate(row)) for row in result_rows.fetchall()]

        if len(result) > 0:
            return result if machineID is None else result[0]
        else:
            return None

    def deleteResults(self, ymdDateString):
        SQL = f"DELETE FROM {src.persistence.RESULT_TABLE}"

        if ymdDateString != "Alle":
            SQL += f" WHERE training_date LIKE '?%'"

        self.cursor.execute(SQL, ymdDateString)
        self.cursor.commit()


    def saveResults(self, machineID, duration, weightDone, weightPlanned, repeats):
        SQL = f"""INSERT OR REPLACE INTO {src.persistence.RESULT_TABLE}
                (
                    customer_id,
                    training_date,
                    machine_id,
                    duration,
                    weight_done,
                    weight_planned
                )
                VALUES(?, ?, ?, ?, ?, ?)
                """

        self.cursor.execute(SQL, [self.customerID,
                    self.timeStamp,
                    machineID,
                    duration,
                    weightDone,
                    weightPlanned,
                    repeats])
        self.cursor.commit()


#-------------------------- TEST -------------------------#
if __name__ == "__main__":
    r = Result(customerID=19711)
    print(r.latest(machineID="F1.1"))

