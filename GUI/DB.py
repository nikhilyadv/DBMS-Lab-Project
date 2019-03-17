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

    def validate (self, username, passcode):
        self.cur.execute("SELECT * FROM Users WHERE username=\"{}\" and passcode=\"{}\"".format(username,passcode))
        row = self.cur.fetchall()
        if len(row) == 1 :
            return True
        return False

    def getrole (self, username, passcode):
        self.cur.execute("SELECT * FROM Users WHERE username=\"{}\" and passcode=\"{}\"".format(username,passcode))
        row = self.cur.fetchall()
        return row[0][2]

    def getProductsFromCart (self):
        self.cur.execute ("call getProductsFromCart();")
        rows = self.cur.fetchall ()
        return rows

    def addProductToCart (self, cid, pid, sid, quantity):
        self.cur.execute ("call addProductToCart(\"{}\",\"{}\",\"{}\",{});".format(cid,pid,sid,quantity))
        self.conn.commit()
        return True

    def getProductsFromNameNIL (self, pname):
        self.cur.execute ("call queryProductsRat(\"{}\");".format (pname))
        rows = self.cur.fetchall ()
        return rows

    def getProductsFromLimit (self, pname, lprice, uprice):
        self.cur.execute ("call queryProductsTim(\"{}\",{},{});".format (pname,lprice,uprice))
        rows = self.cur.fetchall ()
        return rows

    def payandmakeorder (self, cnum, badd, cid, sadd):
        self.cur.execute ("call makeorder(\"{}\",\"{}\",\"{}\",\"{}\");".format(cnum,badd,cid,sadd))
        self.conn.commit()
        return True
