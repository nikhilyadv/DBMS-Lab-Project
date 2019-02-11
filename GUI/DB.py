import MySQLdb as sql # install using https://pypi.org/project/mysqlclient/

class DB:
    def __init__ (self, username, passcode):
        self.conn = sql.connect (user = username, password = passcode, db = "AmaKart")
        self.cur = self.conn.cursor ()

    def __del__(self):  # destructor
        self.conn.close()  # close connection

    def updateproduct (self, product_id, supplier_id, price, total_stock) :
        self.cur.execute("UPDATE product set price={}, total_stock={} where product_id=\"{}\" and supplier_id=\"{}\"".format(price, total_stock, product_id, supplier_id))
        self.conn.commit()
        return True

    def addproduct (self, product_id, supplier_id, price, total_stock, description) :
        print ("INSERT INTO product VALUES (\"{}\", \"{}\", {}, {}, \"{}\")".format(product_id, supplier_id, price, total_stock, description))
        self.cur.execute("INSERT INTO product VALUES (\"{}\", \"{}\", {}, {}, \"{}\")".format(product_id, supplier_id, price, total_stock, description))
        self.conn.commit()
        return True

    def validate (self, username, passcode, role) :
        self.cur.execute("SELECT * FROM Users WHERE username=\"{}\" and passcode=\"{}\" and role=\"{}\"".format(username,passcode,role))
        row = self.cur.fetchall()
        if len(row) == 1 :
            return True
        return False
 
    def userExists (self, username) :
        self.cur.execute("SELECT * FROM Users WHERE username=\"{}\"".format(username))
        row = self.cur.fetchall()
        if len(row) == 1 :
            return True
        return False