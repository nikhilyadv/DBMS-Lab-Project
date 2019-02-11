import MySQLdb as sql # install using https://pypi.org/project/mysqlclient/

class DB:
    def __init__ (self, username, passcode):
        self.conn = sql.connect (user = username, password = passcode, db = "AmaKart")
        self.cur = self.conn.cursor ()

    def __del__(self):  # destructor
        self.conn.close()  # close connection

    def updateproduct (self, product_id, supplier_id, price, total_stock)
        self.cur.execute("UPDATE product set price={}, total_stock={} where product_id={} and supplier_id={}".format(price, total_stock, product_id, supplier_id))
        self.conn.commit()
        return true

    def addproduct (self, product_id, supplier_id, price, total_stock, description) :
        self.cur.execute("INSERT INTO product VALUES ({},{},{},{},{})".format(product_id, supplier_id, price, total_stock, description))
        self.conn.commit()
        return true

    def delete(self, id):
        self.cur.execute("DELETE FROM book WHERE id={}".format(id))
        self.conn.commit()
        self.view()

    def search(self, title="", author="", isbn=""):
        self.cur.execute("SELECT * FROM book WHERE title=\"{}\" OR author=\"{}\" OR isbn={}".format(title, author, isbn))
        rows = self.cur.fetchall()
        return rows
    def addUser (self, username, password):
        print ("Meow")