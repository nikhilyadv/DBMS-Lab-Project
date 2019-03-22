import MySQLdb as sql # install using https://pypi.org/project/mysqlclient/

class DB:
    def __init__(self):
        self.conn = sql.connect (user = "root", password = "root", db = "AmaKart")
        self.cur = self.conn.cursor ()
        self.id = "root"
        self.password = "root"
        self.role = "root"

    def __del__(self):  
        self.conn.close()  

    def checkWhetherUserExists (self, username):
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = \"{}\")".format(username))
        row = self.cur.fetchall()
        if row[0][0] == 0:
            return True
        return False

    def switchToRoot (self):
        self.conn = sql.connect (user = "root", password = "root", db = "AmaKart")
        self.cur = self.conn.cursor ()
        self.role = "root"

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
        self.id = username
        self.password = passcode
        self.role = role

    def validate (self, username, passcode):
        OuserRole = self.role
        Oid = self.id
        Opassword = self.password
        self.switchToRoot()
        self.cur.execute("SELECT * FROM Users WHERE username=\"{}\" and passcode=\"{}\"".format(username,passcode))
        row = self.cur.fetchall()
        retBool = False
        if len(row) == 1 :
            retBool = True
        if (OuserRole != "root"):
            self.loginUser(Oid, Opassword, OuserRole)
        return retBool

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

    def seeLatestNPurchases (self, N):
        self.cur.execute ("call seeLatestNPurchases({});".format (N))
        rows = self.cur.fetchall ()
        return rows

    def seePurchasesByDate (self, startYear, startMonth, startDay, endYear, endMonth, endDay):
        startDate = startYear + '-' + startMonth + "-" + startDay
        endDate = endYear + '-' + endMonth + '-' + endDay
        self.cur.execute ("call seePurchasesByDate(\'{}\',\'{}\');".format (startDate,endDate))
        rows = self.cur.fetchall ()
        return rows

    def addReviewP(self, pid, oid, sid, review):
        self.cur.execute ("call addReviewProduct(\"{}\",\"{}\",\"{}\",\"{}\");".format(pid,oid,sid,review))
        rows = self.cur.fetchall ()
        self.conn.commit()
        return True 

    def addRatingP(self, pid, oid, sid, rating):
        self.cur.execute ("call addRatingProduct(\"{}\",\"{}\",\"{}\",\"{}\");".format(pid,oid,sid,rating))
        rows = self.cur.fetchall ()
        self.conn.commit()
        return True 
    
    def addRatingS(self, pid, oid, sid, rating):
        self.cur.execute ("call addRatingSeller(\"{}\",\"{}\",\"{}\",\"{}\");".format(pid,oid,sid,rating))
        rows = self.cur.fetchall ()
        self.conn.commit()
        return True 

    def addReviewS(self, pid, oid, sid, review):
        self.cur.execute ("call addReviewSeller(\"{}\",\"{}\",\"{}\",\"{}\");".format(pid,oid,sid,review))
        rows = self.cur.fetchall () 
        self.conn.commit()
        return True 

    def getReviews(self, pid, sid):
        self.cur.execute ("call ProductReviews(\"{}\",\"{}\");".format(pid,sid))
        rows = self.cur.fetchall () 
        return rows

    def customerUpdateInfo (self, id, password, name, address, phone_number, email_id):
        self.cur.execute ("call custUpdateInfo(\"{}\",\"{}\",\"{}\",\"{}\", \"{}\",\"{}\");".format(id, password, name, address, phone_number, email_id))
        self.conn.commit()
        self.auxcustomerUpdateInfo(id, password)

    # This function is companion to the previous one for updating password in actual mysql table
    def auxcustomerUpdateInfo (self, id, password):
        if (len (password) > 0):
            userRole = self.role
            self.switchToRoot()
            self.cur.execute ("set password for \'{}\' = PASSWORD(\'{}\');".format(id, password))
            self.conn.commit()
            self.loginUser (id, password, userRole)
    

    ##########################################
    ############SELLER FUNCTIONS##############
    ##########################################

    def existProduct (self, pid, selid):
        self.cur.execute ("call sellerCheckExistProd(\"{}\",\"{}\");".format (pid, selid))
        rows = self.cur.fetchall ()
        if (len (rows) == 1):
            return True
        else:
            return False

    def addProduct (self, pid, selid, pname, pimage, price, tstock, pickadd, des):
        self.cur.execute ("call addProduct(\"{}\",\"{}\",\"{}\",\"{}\", \"{}\",\"{}\",\"{}\",\"{}\");".format(pid, selid, pname, pimage, price, tstock, pickadd, des))
        self.conn.commit()

    def updateProductInfo (self, pid, selid, pname, pimage, price, tstock, pickadd, des):
        self.cur.execute ("call updateProductInfo(\"{}\",\"{}\",\"{}\",\"{}\", \"{}\",\"{}\",\"{}\",\"{}\");".format(pid, selid, pname, pimage, price, tstock, pickadd, des))
        self.conn.commit()

    def sellerUpdateInfo (self, id, password, name, address, phone_number, email_id):
        self.cur.execute ("call sellerUpdateInfo(\"{}\",\"{}\",\"{}\",\"{}\", \"{}\",\"{}\");".format(id, password, name, address, phone_number, email_id))
        self.conn.commit()
        self.auxcustomerUpdateInfo(id, password)

    # This function is companion to the previous one for updating password in actual mysql table
    def auxsellerUpdateInfo (self, id, password):
        if (len (password) > 0):
            userRole = self.role
            self.switchToRoot()
            self.cur.execute ("set password for \'{}\' = PASSWORD(\'{}\');".format(id, password))
            self.conn.commit()
            self.loginUser (id, password, userRole)

    def seePastSellingsDuration (self, startYear, startMonth, startDay, endYear, endMonth, endDay):
        startDate = startYear + '-' + startMonth + "-" + startDay
        endDate = endYear + '-' + endMonth + '-' + endDay
        self.cur.execute ("call seeSellingsBetweenDuration(\"{}\",\"{}\");".format(startDate, endDate))
        rows = self.cur.fetchall ()
        return rows

    def seeLatestNSellings(self, n):
        self.cur.execute ("call seeLatestNSellings({});".format(n))
        rows = self.cur.fetchall ()
        return rows
    
    def sellerSimilarProductsPrice(self, pname):
        self.cur.execute ("call selQuerySimProducts(\"{}\");".format(pname))
        rows = self.cur.fetchall ()
        return rows

    def sellerSimilarProductsRating(self, pname):
        self.cur.execute ("call selQueryProductsRat(\"{}\");".format(pname))
        rows = self.cur.fetchall ()
        return rows

    def sellerPastEarnings (self, startYear, startMonth, startDay, endYear, endMonth, endDay):
        startDate = startYear + '-' + startMonth + "-" + startDay
        endDate = endYear + '-' + endMonth + '-' + endDay
        self.cur.execute ("select sellerStatsBetweenDate(\'{}\',\'{}\');".format(startDate, endDate))
        rows = self.cur.fetchall ()
        return rows

    def sellerRating(self, seller_id):
        self.cur.execute ("call getRating(\"{}\");".format(seller_id))
        rows = self.cur.fetchall ()
        return rows

    def seeShippers (self, name):
        self.cur.execute ("select * from shipper where name like \'%{}%\';".format (name))
        rows = self.cur.fetchall ()
        return rows

    def seeSoldButNotShipped (self, seller_id):
        self.cur.execute ("call soldButNotShipped(\"{}\");".format(seller_id))
        rows = self.cur.fetchall ()
        return rows
    
    def shipperExist (self, shipper_id):
        self.cur.execute ("select * from shipper where shipper_id = \'{}\';".format (shipper_id))
        rows = self.cur.fetchall ()
        if (len (rows) == 1):
            return True
        return False

    def shipSoldProduct (self, product_id, order_id, seller_id, shipper_id, date):
        self.cur.execute ("call shipSoldProduct(\"{}\",\"{}\",\"{}\", \"{}\",\"{}\");".format(product_id, order_id, seller_id, shipper_id, date))
        self.conn.commit()


    ##########################################
    ##########SHIPPER FUNCTIONS###############
    ##########################################


    def seeLatestNShipments(self, n):
        self.cur.execute ("call seeLatestNShipments({});".format(n))
        rows = self.cur.fetchall ()
        return rows



    def seeShipmentsBetweenDuration (self, startYear, startMonth, startDay, endYear, endMonth, endDay):
        startDate = startYear + '-' + startMonth + "-" + startDay
        endDate = endYear + '-' + endMonth + '-' + endDay
        self.cur.execute ("call seeShipmentsBetweenDuration(\"{}\",\"{}\");".format(startDate, endDate))
        rows = self.cur.fetchall ()
        return rows


    def seeDetailedShipments(self):
        self.cur.execute ("select * from shipperTrack;")
        rows = self.cur.fetchall ()
        return rows