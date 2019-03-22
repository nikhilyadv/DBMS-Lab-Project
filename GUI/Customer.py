from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import datetime
import requests
import LoginWindow

class Customer:
    def __init__ (self, db, username):
        self.customer_id = username
        self.db = db
        self.basic()
    def on_closing(self, _window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()
    def on_closingwithoutwarning(self, _window):
        _window.destroy()
    def switchToBasic(self,_window):
        _window.destroy()
        self.basic()
    def switchToCart (self, _window):
        _window.destroy ()
        self.Cart ()
    def switchToBrowse (self, _window):
        _window.destroy ()
        self.browse ()
    def switchToPreviousOrders (self, _window):
        _window.destroy ()
        self.previousOrders ()
    def switchToUpdate (self, _window):
        _window.destroy ()
        self.updateInfo ()
    def switchToLogin (self, _window):
        _window.destroy ()
        LoginWindow.LoginWindow ()

    def basic (self):
        win = Tk ()
        win.title ("Welcome Home Page")
        win.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (win))
        Button(win, text= 'Goto Cart', command= lambda: self.switchToCart (win)).grid(row=1, column=0)
        Button(win, text= 'Browse Products', command= lambda: self.switchToBrowse (win)).grid(row=2, column=0)
        Button (win, text = 'Previous Orders', command = lambda : self.switchToPreviousOrders (win)).grid (row=3, column=0)
        Button(win, text= 'Update your info', command= lambda: self.switchToUpdate (win)).grid(row=4, column=0)
        Button (win, text = 'Back to Login', command = lambda : self.switchToLogin (win)).grid (row=5, column=0)
        win.mainloop ()

    def Cart (self):
        cartwin = Tk ()
        cartwin.title ("Cart")
        cartwin.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (cartwin))
        plist = ttk.Treeview (cartwin)
        ttk.Style().configure('PViewStyle.Treeview', rowheight=60)
        plist = ttk.Treeview (cartwin, style='PViewStyle.Treeview')
        scbVDirSel = Scrollbar(cartwin, orient=VERTICAL, command=plist.yview)
        scbVDirSel.grid(row=1, column=100, rowspan=50, sticky=NS, in_=cartwin)
        plist.configure(yscrollcommand=scbVDirSel.set) 

        plist['columns'] = ('pid', 'pname', 'sellerid', 'price', 'quantity')
        plist.heading ('#0', text = 'Image')
        plist.heading ('pid', text = 'Product ID')
        plist.heading ('pname', text = 'Product Name')
        plist.heading ('sellerid', text = 'Seller ID')
        plist.heading ('price', text = 'Price')
        plist.heading ('quantity', text = 'Quantity')
        plist.grid(row = 1, column = 0, rowspan = 18, columnspan = 100)
        self.populateProductsforCart (plist)
        def purchase ():
            purchwin = Tk()
            purchwin.title ("Make Order")
            purchwin.protocol("WM_DELETE_WINDOW", lambda: ())

            card_number = StringVar(purchwin, value="1234567890")
            billing_address = StringVar(purchwin, value="RM123")
            shipping_address = StringVar(purchwin, value="RM123")

            Label(purchwin, text="Card number").grid(row=0, column=0)
            Entry(purchwin, textvariable=card_number).grid(row=0, column=1)

            Label(purchwin, text="Billing Address").grid(row=1, column=0)
            Entry(purchwin, textvariable=billing_address).grid(row=1, column=1)

            Label(purchwin, text="Shipping Address").grid(row=2, column=0)
            Entry(purchwin, textvariable=shipping_address).grid(row=2, column=1)
            
            def checkandclose(cnum,badd,sadd):
                if (cnum != "") and (badd != "") and (sadd != ""):
                    self.db.payandmakeorder(cnum,badd,self.customer_id,sadd)
                    purchwin.destroy()
                    self.switchToBasic (cartwin)
            Button(purchwin, text= 'Proceed', command= lambda: checkandclose(card_number.get(), billing_address.get(), shipping_address.get())).grid(row=3, column=1, sticky=W)
            purchwin.mainloop()

        Button (cartwin, text = 'Checkout cart', command = lambda: purchase ()).grid (row = 20, sticky = W, pady = 4)
        cartwin.mainloop ()

    def populateProductsforCart (self, plist):
        rows = self.db.getProductsFromCart ()
        plist.delete (*plist.get_children ())
        plist._images = []
        for row in rows:
            auximage = Image.open (requests.get(row[5], stream = True).raw)
            auximage.thumbnail((100, 200), Image.ANTIALIAS)
            auximage = ImageTk.PhotoImage (auximage)
            plist._images.append(auximage)
            plist.insert ('', 'end', values = (row[0], row[4], row[1], row[6], row[3], row[6]), image = plist._images[-1])

    def populateProducts (self, productName, plist):
        rows = self.db.getProductsFromNameNIL(productName)
        plist.delete (*plist.get_children ())
        plist._images = []
        for row in rows:
            auximage = Image.open (requests.get(row[2], stream = True).raw)
            auximage.thumbnail((100, 200), Image.ANTIALIAS)
            auximage = ImageTk.PhotoImage (auximage)
            plist._images.append(auximage)
            plist.insert ('', 'end', values = (row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8]), image = plist._images[-1])

    def populateProductsByLimit (self, productName, lprice, uprice, plist):
        rows = self.db.getProductsFromLimit(productName, lprice, uprice)
        plist.delete (*plist.get_children ())
        plist._images = []
        for row in rows:
            auximage = Image.open (requests.get(row[2], stream = True).raw)
            auximage.thumbnail((100, 200), Image.ANTIALIAS)
            auximage = ImageTk.PhotoImage (auximage)
            plist._images.append(auximage)
            plist.insert ('', 'end', values = (row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8]), image = plist._images[-1])

    def browse (self):
        browseWin = Tk ()
        browseWin.title ("Browse Products")
        browseWin.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (browseWin)) 
        Label(browseWin, text = "Enter product name").grid (row = 0, column = 0, sticky = W)
        Label(browseWin, text = "Lower Price Limit").grid (row = 1, column = 0, sticky = W)
        Label(browseWin, text = "Uper Price Limit").grid (row = 1, column = 2, sticky = W)

        prodText = StringVar()
        lowprice = DoubleVar()
        upprice = DoubleVar()
        Entry(browseWin, textvariable=prodText).grid (row = 0, column = 1, sticky = W)
        Entry(browseWin, textvariable=lowprice).grid (row = 1, column = 1, sticky = W)
        Entry(browseWin, textvariable=upprice).grid (row = 1, column = 3, sticky = W)
        upprice.set(1000.0)
        Button (browseWin, text = 'Switch to Login', command = lambda: self.switchToLogin (browseWin)).grid (row = 21, sticky = W, pady = 4)
        output = Text (browseWin, height = 1, width = 150, wrap = WORD, bg = "white")
        output.grid (row = 21, column = 1, columnspan = 1000)

        ttk.Style().configure('PViewStyle.Treeview', rowheight=60)
        plist = ttk.Treeview (browseWin, style='PViewStyle.Treeview')
        scbVDirSel =Scrollbar(browseWin, orient=VERTICAL, command=plist.yview)
        scbVDirSel.grid(row=2, column=100, rowspan=50, sticky=NS, in_=browseWin)
        plist.configure(yscrollcommand=scbVDirSel.set) 

        plist['columns'] = ('pid', 'pname', 'sellerid', 'price', 'tstock', 'pickupaddress', 'description', 'rating')
        plist.heading ('#0', text = 'Image')
        plist.heading ('pid', text = 'Product ID')
        plist.heading ('pname', text = 'Product Name')
        plist.heading ('sellerid', text = 'Seller ID')
        plist.heading ('price', text = 'Price')
        plist.heading ('tstock', text = 'Total Stock')
        plist.heading ('pickupaddress', text = 'Pickup Address')
        plist.heading ('description', text = 'Description')
        plist.heading ('rating', text = 'Rating')
        plist.grid(row = 2, column = 0, rowspan = 18, columnspan = 100)
        Button(browseWin, text= 'Search by name', command= lambda: self.populateProducts (prodText.get (), plist)).grid(row=0, column=2, sticky=W)
        Button(browseWin, text= 'Search by name & limit', command= lambda: self.populateProductsByLimit (prodText.get (), lowprice.get (), upprice.get (), plist)).grid(row=1, column=5, sticky=W)
        def selectItem(a):
            def check(output, quantity, pid, sid, q):
                if quantity > 0:
                    self.db.addProductToCart(self.customer_id, pid, sid, quantity)
                    if (q >= quantity):
                        tempstr = "Added successfully"
                    else :
                        tempstr = "Please Reduce quantity"
                    output.delete (0.0, END)
                    output.insert (END, tempstr)                    
                else:
                    tempstr = "Wrong quantity entered Please enter a positive interger less then quantity of the product avaliable\n"
                    output.delete (0.0, END)
                    output.insert (END, tempstr)
            def seereviews(pid,sid):
                wint = Tk()
                wint.title("Old Reviews and Rating for products")
                Label(wint, text = ("Product id - " + str(pid) + " and Seller id - " + str(sid))).grid (row = 0, column = 0)
                rows = self.db.getReviews(pid,sid)
                # print (rows)
                rlist = ttk.Treeview (wint, style='PViewStyle.Treeview')
                scbVDirSel =Scrollbar(wint, orient=VERTICAL, command=plist.yview)
                scbVDirSel.grid(row=1, column=100, rowspan=50, sticky=NS, in_=wint)
                rlist.configure(yscrollcommand=scbVDirSel.set) 

                rlist['columns'] = ('prat', 'prev', 'srat', 'srev')
                rlist.heading ('#0', text = 'Customer Name')
                rlist.heading ('prat', text = 'Product Rating')
                rlist.heading ('prev', text = 'Product Review')
                rlist.heading ('srat', text = 'Seller Rating')
                rlist.heading ('srev', text = 'Seller Review')
                rlist.grid(row = 1, column = 0, rowspan = 5, columnspan = 100)
                rlist.delete (*rlist.get_children ())
                for row in rows:
                    rlist.insert ('', 'end', text=row[0], values = (row[1], row[2], row[3], row[4]))
                
            curItem = plist.focus()
            selectedrow = plist.item(curItem)
            if (len(selectedrow['values']) > 0):
                quantityText = IntVar()
                Label(browseWin, text = "Enter Quantity").grid (row = 20, column = 0, sticky = W)
                Entry(browseWin, textvariable=quantityText).grid (row = 20, column = 1, sticky = W)
                quantityText.set(1)
                Button(browseWin, text= 'Add to cart', command= lambda: check(output, quantityText.get (), selectedrow['values'][0], selectedrow['values'][2], selectedrow['values'][4])).grid(row=20, column = 2, sticky = W)
                Button(browseWin, text= 'Check Reviews', command= lambda: seereviews(selectedrow['values'][0],selectedrow['values'][2])).grid(row=20, column = 3, sticky = W)
                # print (plist.item(curItem))
        plist.bind('<ButtonRelease-1>', selectItem)
        browseWin.mainloop()

    def previousOrders (self):
        win = Tk ()
        win.title ("Purchased Products")
        win.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (win)) 

        Label(win, text = "Start Year").grid (row = 0, column = 0, sticky = W)
        Label(win, text = "Start Month").grid (row = 0, column = 2, sticky = W)
        Label(win, text = "Start Day").grid (row = 0, column = 4, sticky = W)
        Label(win, text = "End Year").grid (row = 1, column = 0, sticky = W)
        Label(win, text = "End Month").grid (row = 1, column = 2, sticky = W)
        Label(win, text = "End Day").grid (row = 1, column = 4, sticky = W)
        Label(win, text = "N").grid(row=2, column=0, sticky=W)
        month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        year = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
        day = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]  


        startYear = StringVar ()
        startYear.set(year[0])
        startMonth = StringVar ()
        startMonth.set(month[0])
        startDay = StringVar ()
        startDay.set(day[0])
        endYear = StringVar ()
        endYear.set(year[0])
        endMonth = StringVar ()
        endMonth.set(month[0])
        endDay = StringVar ()
        endDay.set(day[0])
        N = IntVar()
        N.set(1)

        OptionMenu(win, startYear, *year).grid(row = 0, column = 1, sticky = W)
        OptionMenu(win, startMonth, *month).grid(row = 0, column = 3, sticky = W)
        OptionMenu(win, startDay, *day).grid(row = 0, column = 5, sticky = W)
        OptionMenu(win, endYear, *year).grid(row = 1, column = 1, sticky = W)
        OptionMenu(win, endMonth, *month).grid(row = 1, column = 3, sticky = W)
        OptionMenu(win, endDay, *day).grid(row = 1, column = 5, sticky = W)
        Entry(win, textvariable=N).grid (row = 2, column = 1, sticky = W)

        output = Text (win, height = 1, width = 150, wrap = WORD, bg = "white")
        output.grid (row = 23, column = 1, columnspan = 1000)

        ttk.Style().configure('PViewStyle.Treeview', rowheight=60)
        plist = ttk.Treeview (win, style='PViewStyle.Treeview')
        scbVDirSel =Scrollbar(win, orient=VERTICAL, command=plist.yview)
        scbVDirSel.grid(row=3, column=100, rowspan=50, sticky=NS, in_=win)
        scbHDirSel =Scrollbar(win, orient=HORIZONTAL, command=plist.xview)
        scbHDirSel.grid(row=21, column=0, columnspan=250, sticky=EW)
        plist.configure(yscrollcommand=scbVDirSel.set,xscrollcommand=scbHDirSel.set)  

        def validDate(year, month, day):
            correctDate = None
            try:
                newDate = datetime.datetime(year, month, day)
                correctDate = True
            except ValueError:
                correctDate = False
            return correctDate

        def populatebyDate(years, months, days, yeare, monthe, daye, plist):
            strng = ""
            if (validDate (int(years), int(months), int(days)) and validDate (int(yeare), int(monthe), int(daye))):
                rows = self.db.seePurchasesByDate(years, months, days, yeare, monthe, daye)
                plist.delete (*plist.get_children ())
                plist._images = []
                for row in rows:
                    auximage = Image.open (requests.get(row[17], stream = True).raw)
                    auximage.thumbnail((100, 200), Image.ANTIALIAS)
                    auximage = ImageTk.PhotoImage (auximage)
                    plist._images.append(auximage)
                    plist.insert ('', 'end', values = (row[2], row[0], row[16], row[1], row[15], row[14], row[25], row[10], row[9], row[13], row[12]), image = plist._images[-1])
                strng = "Done!"
                # print (rows)
            else:
                strng = "Entered date is not valid!"

            output.delete (0.0, END)
            output.insert (END, strng)                    

        def populatebyN(N,plist):
            strng = ""
            if (N <= 0):
                strng = "Please enter valid N"
            else:
                rows = self.db.seeLatestNPurchases(N)
                plist.delete (*plist.get_children ())
                plist._images = []
                for row in rows:
                    auximage = Image.open (requests.get(row[17], stream = True).raw)
                    auximage.thumbnail((100, 200), Image.ANTIALIAS)
                    auximage = ImageTk.PhotoImage (auximage)
                    plist._images.append(auximage)
                    plist.insert ('', 'end', values = (row[2],row[0], row[16], row[1], row[15], row[14], row[25], row[10], row[9], row[13], row[12]), image = plist._images[-1])
                strng = "Done"

            output.delete (0.0, END)
            output.insert (END, strng)                    

        plist['columns'] = ('oid', 'pid','pname', 'sellerid', 'price', 'quantity', 'status', 'srating', 'prating', 'sreview', 'preview')
        plist.column('#0',anchor="center",width=130,minwidth=130)
        for i in plist['columns']:
            plist.column(i, anchor="center", width=120, minwidth=130)
        plist.heading ('#0', text = 'Image')
        plist.heading ('oid', text = 'Order ID')
        plist.heading ('pid', text = 'Product ID')
        plist.heading ('pname', text = 'Product Name')
        plist.heading ('sellerid', text = 'Seller ID')
        plist.heading ('price', text = 'Price')
        plist.heading ('quantity', text = 'Quantity')
        plist.heading ('status', text = 'Tracking ID')
        # plist.heading ('pickupaddress', text = 'Pickup Address')
        # plist.heading ('description', text = 'Description')
        plist.heading ('srating', text = 'Your Seller Rating')        
        plist.heading ('prating', text = 'Your Product Rating')
        plist.heading ('sreview', text = 'Your Seller Review')        
        plist.heading ('preview', text = 'Your Product Review')
        plist.grid(row = 3, column = 0, rowspan = 18, columnspan = 100)
        # plist.pack(expand=Y)

        Button(win, text= 'Search by Date', command= lambda: (populatebyDate (startYear.get(), startMonth.get(), startDay.get(), endYear.get(), endMonth.get(), endDay.get(), plist))).grid(row=1, column=6, sticky=W, pady=4)
        Button(win, text= 'Search Last N purchases', command= lambda: (populatebyN(N.get(), plist))).grid(row=2, column=3, sticky=W, pady=4)
        def selectItem(a):
            curItem = plist.focus()
            selectedrow = plist.item(curItem)
            if (len(selectedrow['values']) > 0):
                # print (selectedrow)
                def addReviewP(pid,oid,sid):
                    wint = Tk()
                    wint.title("Review")

                    Label(wint, text = "Write Review").grid(row = 0, column = 0, sticky = W) 
                    rev = StringVar (wint)
                    Entry(wint, textvariable=rev).grid(row = 1, column = 0, rowspan=5, sticky = W)

                    def closeandcall (r):
                        # print(rev.get())
                        self.db.addReviewP(pid,oid,sid,r)
                        wint.destroy()

                    Button(wint, text= 'Add', command= lambda: closeandcall(rev.get())).grid(row=6, sticky=W)
                    wint.mainloop()

                def addReviewS(pid,oid,sid):
                    wint = Tk()
                    wint.title("Review")

                    Label(wint, text = "Write Review").grid(row = 0, column = 0) 
                    rev = StringVar (wint)
                    Entry(wint, textvariable=rev).grid(row = 1, column = 0, rowspan=5)

                    def closeandcall (r):
                        # print(rev.get())
                        self.db.addReviewS(pid,oid,sid,r)
                        wint.destroy()

                    Button(wint, text= 'Add', command= lambda: closeandcall(rev.get())).grid(row=6)
                    wint.mainloop()

                def addRatingP(pid,oid,sid):
                    wint = Tk()
                    wint.title("Rating")

                    Label(wint, text = "Choose Rating").grid(row=0, column=0)
                    ratlist = [1,2,3,4,5]
    
                    rat = IntVar(wint)

                    OptionMenu(wint, rat, *ratlist).grid(row = 1, column = 0)

                    def closeandcall (r):
                        # print (r)
                        self.db.addRatingP(pid,oid,sid,r)
                        wint.destroy()

                    Button(wint, text= 'Add', command= lambda: closeandcall(rat.get())).grid(row=6)
                    wint.mainloop()

                def addRatingS(pid,oid,sid):
                    wint = Tk()
                    wint.title("Rating")

                    Label(wint, text = "Choose Rating").grid(row=0, column=0)
                    ratlist = [1,2,3,4,5]
    
                    rat = IntVar(wint)

                    OptionMenu(wint, rat, *ratlist).grid(row = 1, column = 0)

                    def closeandcall (r):
                        # print (r)
                        self.db.addRatingS(pid,oid,sid,r)
                        wint.destroy()

                    Button(wint, text= 'Add', command= lambda: closeandcall(rat.get())).grid(row=6)
                    wint.mainloop()

                Button(win, text= 'Add/Update Rating for Product', command= lambda: (addRatingP(selectedrow['values'][1],selectedrow['values'][0],selectedrow['values'][3]))).grid(row=24, column = 0, sticky = W)
                Button(win, text= 'Add/Update Rating for Seller', command= lambda: (addRatingS(selectedrow['values'][1],selectedrow['values'][0],selectedrow['values'][3]))).grid(row=24, column = 1, sticky = W)
                Button(win, text= 'Add/Update Review for Product', command= lambda: (addReviewP(selectedrow['values'][1],selectedrow['values'][0],selectedrow['values'][3]))).grid(row=24, column = 2, sticky = W)
                Button(win, text= 'Add/Update Review for Seller', command= lambda: (addReviewS(selectedrow['values'][1],selectedrow['values'][0],selectedrow['values'][3]))).grid(row=24, column = 3, sticky = W)
        plist.bind('<ButtonRelease-1>', selectItem)
        win.mainloop()

    def updateInfo (self):
        sign = Tk ()
        sign.title ("Update Info (You must enter your previous password and in case you don't want to change any of the respective info then leave that field empty or as it is)")
        sign.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (sign))  # handle window closing
        output = Text (sign, height = 1, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 7, column = 1)
        Label(sign, text = "Previous Password").grid (row = 0, column = 0, sticky = W)
        Label(sign, text = "New Password (can be same as old one) - leave this field empty if you don't want to change your password").grid (row = 1, column = 0, sticky = W)
        Label(sign, text = "Repeat New Password - again, leave this field empty if you don't want wish to change your password").grid (row = 2, column = 0, sticky = W)
        Label(sign, text = "Name").grid (row = 3, column = 0, sticky = W)
        Label(sign, text = "Address").grid (row = 4, column = 0, sticky = W)
        Label(sign, text = "Phone number").grid (row = 5, column = 0, sticky = W)
        Label(sign, text = "email-id").grid (row = 6, column = 0, sticky = W)

        prevPassText = StringVar()
        passText = StringVar ()
        repPassText = StringVar ()
        name = StringVar ()
        add = StringVar ()
        phone = IntVar ()
        email = StringVar ()

        Entry(sign, textvariable=prevPassText, show = "*").grid (row = 0, column = 1, sticky = W)
        Entry(sign, textvariable=passText, show = "*").grid (row = 1, column = 1, sticky = W)
        Entry(sign, textvariable=repPassText, show = "*").grid (row = 2, column = 1, sticky = W)
        Entry(sign, textvariable=name).grid (row = 3, column = 1, sticky = W)
        Entry(sign, textvariable=add).grid (row = 4, column = 1, sticky = W)
        Entry(sign, textvariable=phone).grid (row = 5, column = 1, sticky = W)
        Entry(sign, textvariable=email).grid (row = 6, column = 1, sticky = W)
        def fine (x):
            if (len (x) > 0): 
                return True
            else:
                return False
        def check (password, npassword, rnpassword, name, add, phone, email):
            strng = "Update successful"
            if (fine(password) and self.db.validate (self.customer_id, password)):
                if ((fine(npassword) and npassword == rnpassword) or not fine(npassword)):
                    self.db.customerUpdateInfo(self.customer_id, npassword, name, add, phone, email)
                    strng = "Update successful"
                else:
                    strng = "You have issue with new password"
            else:
                strng = "Previous password not correctly entered"
            
            output.delete (0.0, END)
            output.insert (END, strng)
        Button(sign, text= 'Update', command= lambda: check (prevPassText.get (), passText.get (), repPassText.get (), name.get (), add.get (), phone.get (), email.get ())).grid(row=8, sticky=W, pady=4)
        Button (sign, text = 'Switch to Login', command = lambda: self.switchToLogin (sign)).grid (row = 9, sticky = W, pady = 4)
        sign.mainloop()