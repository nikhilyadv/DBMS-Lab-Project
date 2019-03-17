from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
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
        Button(win, text= 'Goto Cart', command= lambda: self.switchToCart (win)).grid(row=1, column=0, sticky=W)
        Button(win, text= 'Browse Products', command= lambda: self.switchToBrowse (win)).grid(row=2, column=0, sticky=W)
        Button (win, text = 'Previous Orders', command = lambda : self.switchToPreviousOrders (win)).grid (row=3, column=0, sticky = W)
        Button(win, text= 'Update your info', command= lambda: self.switchToUpdate (win)).grid(row=4, column=0, sticky=W)
        Button (win, text = 'Back to Login', command = lambda : self.switchToLogin (win)).grid (row=5, column=0, sticky = W)
        win.mainloop ()

    def Cart (self):
        cartwin = Tk ()
        cartwin.title ("Cart")
        cartwin.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (cartwin))
        plist = ttk.Treeview (cartwin)
        ttk.Style().configure('PViewStyle.Treeview', rowheight=60)
        plist = ttk.Treeview (cartwin, style='PViewStyle.Treeview')
        scbVDirSel =Scrollbar(cartwin, orient=VERTICAL, command=plist.yview)
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
            curItem = plist.focus()
            selectedrow = plist.item(curItem)
            quantityText = IntVar()
            Label(browseWin, text = "Enter Quantity").grid (row = 20, column = 0, sticky = W)
            Entry(browseWin, textvariable=quantityText).grid (row = 20, column = 1, sticky = W)
            quantityText.set(1)
            Button(browseWin, text= 'Add to cart', command= lambda: check(output, quantityText.get (), selectedrow['values'][0], selectedrow['values'][2], selectedrow['values'][4])).grid(row=20, column = 2, sticky = W)
            # print (plist.item(curItem))
        plist.bind('<ButtonRelease-1>', selectItem)
        browseWin.mainloop()

    def previousOrders (self):
        # TODO
        self.basic ()

    def updateInfo (self):
        # TODO
        self.basic ()