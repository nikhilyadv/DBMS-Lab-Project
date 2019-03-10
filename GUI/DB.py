import MySQLdb as sql # install using https://pypi.org/project/mysqlclient/

class DB:
    def __init__(self):
        self.conn = sql.connect (user = "root", password = "root", db = "AmaKart")
        self.cur = self.conn.cursor ()

    def __del__(self):  
        self.conn.close()  

    def checkWhetherUserExists (self, username):
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = \"{}\")".format(username))
        row = self.cur.fetchall()
        if row[0][0] == 0:
            return True
        return False
 
    def createUser (self, username, passcode, role, name, address, phonenumber, email):
        if self.checkWhetherUserExists(username) == False:
            return False
        self.cur.execute("INSERT INTO Users VALUES (\"{}\", \"{}\", \"{}\")".format(username, passcode, role))
        self.conn.commit()
        self.cur.execute("CREATE USER {} IDENTIFIED BY \"{}\";".format(username, passcode))
        
        self.conn.commit()
        self.cur.execute("GRANT {} to {}".format(role, username))
        self.conn.commit()
        if (role == "seller"):
            self.cur.execute("INSERT INTO {} VALUES(\"{}\",\"{}\",\"{}\",{},\"{}\", NULL);".format(role, username, name, address, phonenumber, email)) 
        else:
            self.cur.execute("INSERT INTO {} VALUES(\"{}\",\"{}\",\"{}\",{},\"{}\");".format(role, username, name, address, phonenumber, email))
        self.conn.commit()
        return True
 
    def loginUser (self, username, passcode, role):
        self.conn = sql.connect (user = username, password = passcode)
        self.cur = self.conn.cursor ()
        self.cur.execute("SET ROLE {};".format(role))
        self.conn.commit ()
        self.cur.execute("use AmaKart;")
        self.conn.commit ()

    def validate (self, username, passcode, role) :
        self.cur.execute("SELECT * FROM Users WHERE username=\"{}\" and passcode=\"{}\" and roles=\"{}\"".format(username,passcode,role))
        row = self.cur.fetchall()
        if len(row) == 1 :
            return True
        return False
    # left for reference as of now.
    def _hi(self):
        self.cur.execute ("call getDetails();")
        row = self.cur.fetchall()
        print ("I am pri")
        print (row)
        print ("\n")
    ######################################################
    ###########CUSTOMER FUNCTIONS#########################
    ######################################################
    def getProductsFromNameNIL(self, pname):
        self.cur.execute ("call queryProductsRat(\"{}\");".format (pname))
        rows = self.cur.fetchall ()
        return rows
   
"""    def updateInfo (self, username, passcode, name, address, phonenumber, email):
        self.cur.execute("UPDATE customer_add ;".format(username, passcode))
        self.conn.commit()"""
    
    
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