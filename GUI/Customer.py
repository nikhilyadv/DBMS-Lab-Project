from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import LoginWindow

class Customer:
    def __init__ (self, db, username):
        self.customer_id = username
        self.db = db
        self.basic()
    def on_closing(self, _window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()
    def switchToLogin (self, _window):
        _window.destroy ()
        LoginWindow.LoginWindow (self.db)
    def switchToBrowse (self, _window):
        _window.destroy ()
        self.browse ()
    def switchToUpdate (self, _window):
        _window.destroy ()
        self.updateInfo ()
    def switchToPreviousOrders (self, _window):
        _window.destroy ()
        self.previousOrders ()
    def updateInfo (self):
        # TODO
        self.basic ()
    def previousOrders (self):
        # TODO
        self.basic ()
    def basic (self):
        win = Tk ()
        win.title ("Welcome")
        win.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (win))  # handle window closing
        Button(win, text= 'Browse Products', command= lambda: self.switchToBrowse (win)).grid(row=1, column = 0, sticky=W)
        Button(win, text= 'Update your info', command= lambda: self.switchToUpdate (win)).grid(row=2, column = 0, sticky=W)
        Button (win, text = 'Back to Login', command = lambda : self.switchToLogin (win)).grid (row = 3, column = 0, sticky = W)
        Button (win, text = 'Previous Orders', command = lambda : switchToPreviousOrders (win)).grid (row = 4, column = 0, sticky = W)
        win.mainloop ()
    def populateProducts (self, productName, plist):
        rows = self.db.getProductsFromNameNIL(productName)
        auximage = Image.open ("/home/sourabh/Documents/Github/DBMS-Lab-Project/TkinterReference/small.png")
        self.auxphoto = ImageTk.PhotoImage (auximage)
        plist.delete (*plist.get_children ())
        for row in rows:
            print (row)
            plist.insert ('', 'end', text = '#0s text', values = row, image = self.auxphoto)
    def browse (self):
        browseWin = Tk ()
        browseWin.title ("Browse Products")
        browseWin.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (browseWin))  # handle window closing
        Label(browseWin, text = "Enter product name").grid (row = 0, column = 0, sticky = W)

        prodText = StringVar()

        Entry(browseWin, textvariable=prodText).grid (row = 0, column = 1, sticky = W)
        Button (browseWin, text = 'Switch to Login', command = lambda: self.switchToLogin (browseWin)).grid (row = 20, sticky = W, pady = 4)
        ############ Product List #############
        plist = ttk.Treeview (browseWin)
        plist['columns'] = ('pid', 'pname', 'sellerid', 'price', 'tstock', 'pickupaddress', 'description', 'rating')
        plist.heading('#0', text = 'Pic directory', anchor = 'center')
        plist.column ('#0', anchor = 'w', width = 200)
        plist.heading ('pid', text = 'Product ID')
        plist.heading ('pname', text = 'Product Name')
        plist.heading ('sellerid', text = 'Seller ID')
        plist.heading ('price', text = 'Price')
        plist.heading ('tstock', text = 'Total Stock')
        plist.heading ('pickupaddress', text = 'Pickup Address')
        plist.heading ('description', text = 'Description')
        plist.heading ('rating', text = 'Rating')
        plist['show'] = 'headings'
        plist.grid(row = 1, column = 0, rowspan = 18, columnspan = 50)
        Button(browseWin, text= 'Search', command= lambda: self.populateProducts (prodText.get (), plist)).grid(row=0, column = 2, sticky=W)
        browseWin.mainloop()