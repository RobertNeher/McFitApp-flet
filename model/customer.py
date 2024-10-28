import src.persistence as persistence

class Customer:
    def __init__(self, customer_id):
        db = persistence.DBConnection(initialize=False)
        customers = db.connection.execute(f"""SELECT name FROM {persistence.CUSTOMER_TABLE}
                                            WHERE customer_id = {customer_id}""")

        result = customers.fetchone()
        self.full_name = result[0] if result else None

#-------------------------- TEST -------------------------#
if __name__ == "__main__":
    c = Customer("TÜ001-6876582")
    print(c.full_name)
