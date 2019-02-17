import MySQLdb as sql # install using https://pypi.org/project/mysqlclient/

class DB:
    def __del__(self):  
        self.conn.close()  

    def createUser (self, username, passcode, role):
        self.login("root","root","norole")
        self.cur.execute("CREATE USER {} IDENTIFIED BY \"{}\";".format(username, passcode))
        self.conn.commit()
        self.cur.execute("GRANT {} to {}".format(role, username))
        self.conn.commit()

    def login (self, username, passcode, role):
        self.conn = sql.connect (user = username, password = passcode, db = "AmaKart")
        self.cur = self.conn.cursor ()
        if (role != "norole"):
            self.cur.execute("SET ROLE {};".format(role))
    
    
"""
    def updateproduct (self, product_id, supplier_id, price, total_stock) :
        self.cur.execute("UPDATE product set price={}, total_stock={} where product_id=\"{}\" and supplier_id=\"{}\"".format(price, total_stock, product_id, supplier_id))
        self.conn.commit()
        return True

    def addproduct (self, product_id, supplier_id, price, total_stock, description) :
        self.cur.execute("INSERT INTO product VALUES (\"{}\", \"{}\", {}, {}, \"{}\")".format(product_id, supplier_id, price, total_stock, description))
        self.conn.commit()
        return True

    def addUser (self, username, passcode, name, address, phone, email, role) :
        self.cur.execute("INSERT INTO Users VALUES (\"{}\", \"{}\", \"{}\")".format(username, passcode, role))
        self.conn.commit()
        table_name = ""
        if role == "CUS":
            table_name = "customer"
        elif role == "SUP":
            table_name = "supplier"
        elif role == "SHI":
            table_name = "shipper"
        self.cur.execute("INSERT INTO {} VALUES (\"{}\", \"{}\", \"{}\", {}, \"{}\")".format(table_name, username, name, address, phone, email))
        self.conn.commit()

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
"""