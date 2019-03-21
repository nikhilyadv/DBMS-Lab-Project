from tkinter import *
from tkinter import messagebox

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
    
    def newprod (self):
        prod = Tk()
        prod.title("Add Product")
        prod.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (prod))

        def add(product_id, seller_id, price, total_stock, description):
            self.db.addproduct (product_id, seller_id, price, total_stock, description)
            prod.destroy ()
            self.basic ()
        
        Label(prod, text = "Product Id").grid (row = 0, column = 0, sticky = W)
        Label(prod, text = "Price").grid (row = 0, column = 2, sticky = W)
        Label(prod, text = "Quantity").grid (row = 0, column = 4, sticky = W)
        Label(prod, text = "Description").grid (row = 1, column = 0, sticky = W)

        product_id = StringVar()
        seller_id = self.seller_id
        price = StringVar()
        total_stock = IntVar()
        description = StringVar()

        Entry(prod, textvariable = product_id).grid (row = 0, column = 1, sticky = W)
        Entry(prod, textvariable = price).grid (row = 0, column = 3, sticky = W)
        Entry(prod, textvariable = total_stock).grid (row = 0, column = 5, sticky = W)
        Entry(prod, textvariable = description).grid (row = 1, column = 1, sticky = W)
        print (product_id.get (), seller_id, price.get (), total_stock.get (), description.get (), "\n")
        Button(prod, text = "Add Product", command= lambda: add(product_id.get (), seller_id, price.get (), total_stock.get (), description.get ())).grid (row = 2, column = 0, sticky = W)
        prod.mainloop()
    

    def updateInfo (self):
        win = Tk ()
        win.title ("Update Info (You must enter your previous password and in case you don't want to change any of the respective info then leave that field empty)")
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
        def addnewprods ():
            supp.destroy ()
            self.newprod ()
        Button(supp, text= 'Add new products', command= addnewprods).grid(row=1, column=0)
        Button(supp, text= 'Change existing products information', command= lambda: self.switchToUpdateProd (supp)).grid(row=2, column=0)
        Button(supp, text= 'Update Your Info', command= lambda: self.switchToUpdate (supp)).grid(row=3, column=0)
        supp.mainloop()
