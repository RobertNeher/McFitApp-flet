import src.persistence as persistence

class Customer:
    def __init__(self, customer_id):
        SQL = f"""SELECT name FROM {persistence.CUSTOMER_TABLE} WHERE customer_id = ?"""
        db = persistence.DBConnection(initialize=False)
        cursor = db.connection.cursor()
        customers = cursor.execute(SQL, [customer_id])
        result = customers.fetchall()
        self.full_name = result[0] if result else None

#-------------------------- TEST -------------------------#
if __name__ == "__main__":
    c = Customer("TÜ001-6876582")
    print(c.full_name)
