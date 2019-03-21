from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import requests
import datetime

class Seller:
    def __init__ (self, db, username):
        self.db = db
        self.seller_id = username
        self.basic ()

    def on_closing(self, _window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()

    def switchToBasic(self,_window):
        _window.destroy()
        self.basic()

    def switchToUpdateProd (self, _window):
        _window.destroy ()
        self.updateprod ()

    def switchToUpdate (self, _window):
        _window.destroy ()
        self.updateInfo ()

    def switchToAddProduct (self, _window):
        _window.destroy ()
        self.addProduct ()

    def switchToPastSellingsDuration (self, _window):
        _window.destroy ()
        self.pastSellingsDuration()
    
    def switchToLatestNSellings (self, _window):
        _window.destroy ()
        self.latestNSellings()
    
    def latestNSellings(self):
        win = Tk ()
        win.title ("See latest N Sellings")
        win.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (win)) 

        Label(win, text = "N: (min 1)").grid (row = 0, column = 0, sticky = W)

        n = IntVar ()
        Entry(win, textvariable=n).grid (row = 0, column = 1, sticky = W)

        Button (win, text = 'Switch to Login', command = lambda: self.switchToLogin (win)).grid (row = 21, sticky = W, pady = 4)
        output = Text (win, height = 1, width = 150, wrap = WORD, bg = "white")
        output.grid (row = 21, column = 1, columnspan = 1000)

        ttk.Style().configure('PViewStyle.Treeview', rowheight=60)
        plist = ttk.Treeview (win, style='PViewStyle.Treeview')
        scbVDirSel =Scrollbar(win, orient=VERTICAL, command=plist.yview)
        scbVDirSel.grid(row=2, column=100, rowspan=50, sticky=NS, in_=win)
        plist.configure(yscrollcommand=scbVDirSel.set) 

        def populateProducts (n, plist):
            strng = ""
            if (n > 0):
                rows = self.db.seeLatestNSellings(n)
                plist.delete (*plist.get_children ())
                plist._images = []
                for row in rows:
                    auximage = Image.open (requests.get(row[2], stream = True).raw)
                    auximage.thumbnail((100, 200), Image.ANTIALIAS)
                    auximage = ImageTk.PhotoImage (auximage)
                    plist._images.append(auximage)
                    plist.insert ('', 'end', values = (row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8]), image = plist._images[-1])
                strng = "Done!"
            else:
                strng = "Entered N is not valid!"

            output.delete (0.0, END)
            output.insert (END, strng)                    

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
        Button(win, text= 'Search', command= lambda: populateProducts (n.get(), plist)).grid(row=1, column=7, sticky=W)
        win.mainloop()


    def pastSellingsDuration(self):
        win = Tk ()
        win.title ("See Past Sellings")
        win.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (win)) 

        Label(win, text = "Start Year").grid (row = 0, column = 0, sticky = W)
        Label(win, text = "Start Month").grid (row = 0, column = 2, sticky = W)
        Label(win, text = "Start Day").grid (row = 0, column = 4, sticky = W)
        Label(win, text = "End Year").grid (row = 1, column = 0, sticky = W)
        Label(win, text = "End Month").grid (row = 1, column = 2, sticky = W)
        Label(win, text = "End Day").grid (row = 1, column = 4, sticky = W)

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

        OptionMenu(win, startYear, *year).grid(row = 0, column = 1, sticky = W)
        OptionMenu(win, startMonth, *month).grid(row = 0, column = 3, sticky = W)
        OptionMenu(win, startDay, *day).grid(row = 0, column = 5, sticky = W)
        OptionMenu(win, endYear, *year).grid(row = 1, column = 1, sticky = W)
        OptionMenu(win, endMonth, *month).grid(row = 1, column = 3, sticky = W)
        OptionMenu(win, endDay, *day).grid(row = 1, column = 5, sticky = W)

        Button (win, text = 'Switch to Login', command = lambda: self.switchToLogin (win)).grid (row = 21, sticky = W, pady = 4)
        output = Text (win, height = 1, width = 150, wrap = WORD, bg = "white")
        output.grid (row = 21, column = 1, columnspan = 1000)

        ttk.Style().configure('PViewStyle.Treeview', rowheight=60)
        plist = ttk.Treeview (win, style='PViewStyle.Treeview')
        scbVDirSel =Scrollbar(win, orient=VERTICAL, command=plist.yview)
        scbVDirSel.grid(row=2, column=100, rowspan=50, sticky=NS, in_=win)
        plist.configure(yscrollcommand=scbVDirSel.set) 

        def validDate(year, month, day):
            correctDate = None
            try:
                newDate = datetime.datetime(year, month, day)
                correctDate = True
            except ValueError:
                correctDate = False
            return correctDate

        def populateProducts (years, months, days, yeare, monthe, daye, plist):
            strng = ""
            if (validDate (int(years), int(months), int(days)) and validDate (int(yeare), int(monthe), int(daye))):
                rows = self.db.seePastSellingsDuration(years, months, days, yeare, monthe, daye)
                plist.delete (*plist.get_children ())
                plist._images = []
                for row in rows:
                    auximage = Image.open (requests.get(row[2], stream = True).raw)
                    auximage.thumbnail((100, 200), Image.ANTIALIAS)
                    auximage = ImageTk.PhotoImage (auximage)
                    plist._images.append(auximage)
                    plist.insert ('', 'end', values = (row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8]), image = plist._images[-1])
                strng = "Done!"
            else:
                strng = "Entered date is not valid!"

            output.delete (0.0, END)
            output.insert (END, strng)                    

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
        Button(win, text= 'Search', command= lambda: populateProducts (startYear.get(), startMonth.get(), startDay.get(), endYear.get(), endMonth.get(), endDay.get(), plist)).grid(row=1, column=7, sticky=W)
        win.mainloop()

    def updateprod (self):
        win = Tk ()
        win.title ("Update Info (In case you don't want to change any of the respective info then leave that field empty (or as it is) but clearly you must enter product_id)")
        win.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (win))  # handle window closing
        output = Text (win, height = 3, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 7, column = 1, rowspan = 3)
        Label(win, text = "Product ID").grid (row = 0, column = 0, sticky = W)
        Label(win, text = "Product Name").grid (row = 1, column = 0, sticky = W)
        Label(win, text = "Product Image URL").grid (row = 2, column = 0, sticky = W)
        Label(win, text = "Price").grid (row = 3, column = 0, sticky = W)
        Label(win, text = "Total Stock").grid (row = 4, column = 0, sticky = W)
        Label(win, text = "Pickup Address").grid (row = 5, column = 0, sticky = W)
        Label(win, text = "Description").grid (row = 6, column = 0, sticky = W)

        pid = StringVar()
        pname = StringVar()
        pimage = StringVar()
        price = DoubleVar()
        tstock = IntVar()
        pickadd = StringVar()
        des = StringVar()

        Entry(win, textvariable=pid).grid (row = 0, column = 1, sticky = W)
        Entry(win, textvariable=pname).grid (row = 1, column = 1, sticky = W)
        Entry(win, textvariable=pimage).grid (row = 2, column = 1, sticky = W)
        Entry(win, textvariable=price).grid (row = 3, column = 1, sticky = W)
        Entry(win, textvariable=tstock).grid (row = 4, column = 1, sticky = W)
        Entry(win, textvariable=pickadd).grid (row = 5, column = 1, sticky = W)
        Entry(win, textvariable=des).grid (row = 6, column = 1, sticky = W)
        def fine (x):
            if (len (x) > 0): 
                return True
            else:
                return False
        def check (pid, pname, pimage, price, tstock, pickadd, des):
            strng = ""
            if (fine(pid)):
                self.db.updateProductInfo(pid, self.seller_id, pname, pimage, price, tstock, pickadd, des)
                strng = "Update successful (provied you did have this product_id corresponding to your seller_id)"
            else:
                strng = "No Product ID Entered"
            
            output.delete (0.0, END)
            output.insert (END, strng)
        Button(win, text= 'Update', command= lambda: check (pid.get(), pname.get (), pimage.get (), price.get (), tstock.get (), pickadd.get (), des.get ())).grid(row=12, sticky=W, pady=4)
        Button (win, text = 'Switch to Login', command = lambda: self.switchToLogin (win)).grid (row = 13, sticky = W, pady = 4)
        win.mainloop() 
    
    def addProduct (self):
        win = Tk ()
        win.title ("Add Product (You must enter each field)")
        win.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (win))  # handle window closing
        output = Text (win, height = 3, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 7, column = 1, rowspan = 3)
        Label(win, text = "Product ID").grid (row = 0, column = 0, sticky = W)
        Label(win, text = "Product Name").grid (row = 1, column = 0, sticky = W)
        Label(win, text = "Product Image URL").grid (row = 2, column = 0, sticky = W)
        Label(win, text = "Price (Min Rs 1)").grid (row = 3, column = 0, sticky = W)
        Label(win, text = "Total Stock (Min 1)").grid (row = 4, column = 0, sticky = W)
        Label(win, text = "Pickup Address").grid (row = 5, column = 0, sticky = W)
        Label(win, text = "Description").grid (row = 6, column = 0, sticky = W)

        pid = StringVar()
        pname = StringVar()
        pimage = StringVar()
        price = DoubleVar()
        tstock = IntVar()
        pickadd = StringVar()
        des = StringVar()

        Entry(win, textvariable=pid).grid (row = 0, column = 1, sticky = W)
        Entry(win, textvariable=pname).grid (row = 1, column = 1, sticky = W)
        Entry(win, textvariable=pimage).grid (row = 2, column = 1, sticky = W)
        Entry(win, textvariable=price).grid (row = 3, column = 1, sticky = W)
        Entry(win, textvariable=tstock).grid (row = 4, column = 1, sticky = W)
        Entry(win, textvariable=pickadd).grid (row = 5, column = 1, sticky = W)
        Entry(win, textvariable=des).grid (row = 6, column = 1, sticky = W)
        def fine (x):
            if (len (x) > 0): 
                return True
            else:
                return False
        def check (pid, pname, pimage, price, tstock, pickadd, des):
            strng = ""
            if (fine(pid) and fine(pname) and fine(pimage) and (price > 0.9) and (tstock > 0) and fine(pickadd) and fine(des)):
                if (not self.db.existProduct(pid, self.seller_id)):
                    self.db.addProduct(pid, self.seller_id, pname, pimage, price, tstock, pickadd, des)
                    strng = "Product Added Successfully"
                else:
                    strng = "This product id already exist"
            else:
                strng = "You haven't entered all info required"
            
            output.delete (0.0, END)
            output.insert (END, strng)
        Button(win, text= 'Add', command= lambda: check (pid.get(), pname.get (), pimage.get (), price.get (), tstock.get (), pickadd.get (), des.get ())).grid(row=12, sticky=W, pady=4)
        Button (win, text = 'Switch to Login', command = lambda: self.switchToLogin (win)).grid (row = 13, sticky = W, pady = 4)
        win.mainloop()  
    

    def updateInfo (self):
        win = Tk ()
        win.title ("Update Info (You must enter your previous password and in case you don't want to change any of the respective info then leave that field empty or as it is)")
        win.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (win))  # handle window closing
        output = Text (win, height = 1, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 7, column = 1)
        Label(win, text = "Previous Password").grid (row = 0, column = 0, sticky = W)
        Label(win, text = "New Password (can be same as old one) - leave this field empty if you don't want to change your password").grid (row = 1, column = 0, sticky = W)
        Label(win, text = "Repeat New Password - again, leave this field empty if you don't want wish to change your password").grid (row = 2, column = 0, sticky = W)
        Label(win, text = "Name").grid (row = 3, column = 0, sticky = W)
        Label(win, text = "Address").grid (row = 4, column = 0, sticky = W)
        Label(win, text = "Phone number").grid (row = 5, column = 0, sticky = W)
        Label(win, text = "email-id").grid (row = 6, column = 0, sticky = W)

        prevPassText = StringVar()
        passText = StringVar ()
        repPassText = StringVar ()
        name = StringVar ()
        add = StringVar ()
        phone = IntVar ()
        email = StringVar ()

        Entry(win, textvariable=prevPassText, show = "*").grid (row = 0, column = 1, sticky = W)
        Entry(win, textvariable=passText, show = "*").grid (row = 1, column = 1, sticky = W)
        Entry(win, textvariable=repPassText, show = "*").grid (row = 2, column = 1, sticky = W)
        Entry(win, textvariable=name).grid (row = 3, column = 1, sticky = W)
        Entry(win, textvariable=add).grid (row = 4, column = 1, sticky = W)
        Entry(win, textvariable=phone).grid (row = 5, column = 1, sticky = W)
        Entry(win, textvariable=email).grid (row = 6, column = 1, sticky = W)
        def fine (x):
            if (len (x) > 0): 
                return True
            else:
                return False
        def check (password, npassword, rnpassword, name, add, phone, email):
            strng = "Update successful"
            if (fine(password) and self.db.validate (self.seller_id, password)):
                if ((fine(npassword) and npassword == rnpassword) or not fine(npassword)):
                    self.db.sellerUpdateInfo(self.seller_id, npassword, name, add, phone, email)
                    strng = "Update successful"
                else:
                    strng = "You have issue with new password"
            else:
                strng = "Previous password not correctly entered"
            
            output.delete (0.0, END)
            output.insert (END, strng)
        Button(win, text= 'Update', command= lambda: check (prevPassText.get (), passText.get (), repPassText.get (), name.get (), add.get (), phone.get (), email.get ())).grid(row=8, sticky=W, pady=4)
        Button (win, text = 'Switch to Login', command = lambda: self.switchToLogin (win)).grid (row = 9, sticky = W, pady = 4)
        win.mainloop()





    def basic(self):
        supp = Tk()
        supp.title("Welcome Supplier")
        supp.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (supp))
        Button(supp, text= 'Add new products', command= lambda: self.switchToAddProduct (supp)).grid(row=1, column=0)
        Button(supp, text= 'Change existing products information', command= lambda: self.switchToUpdateProd (supp)).grid(row=2, column=0)
        Button(supp, text= 'Update Your Info', command= lambda: self.switchToUpdate (supp)).grid(row=3, column=0)
        Button(supp, text= 'See You Past Sellings Between Some Duration', command= lambda: self.switchToPastSellingsDuration (supp)).grid(row=4, column=0)
        Button(supp, text= 'See You Latest N Sellings', command= lambda: self.switchToLatestNSellings (supp)).grid(row=5, column=0)
        supp.mainloop()
