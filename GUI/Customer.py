from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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
    def populateProducts (self, productName):
        rows = self.db.getProductsFromNameNIL(productName)
        print (rows)
    def browse (self):
        browseWin = Tk ()
        browseWin.title ("Browse Products")
        browseWin.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (browseWin))  # handle window closing
        Label(browseWin, text = "Enter product name").grid (row = 0, column = 0, sticky = W)

        prodText = StringVar()

        Entry(browseWin, textvariable=prodText).grid (row = 0, column = 1, sticky = W)
        Button(browseWin, text= 'Search', command= lambda: self.populateProducts (prodText.get ())).grid(row=0, column = 2, sticky=W)
        Button (browseWin, text = 'Switch to Login', command = lambda: self.switchToLogin (browseWin)).grid (row = 20, sticky = W, pady = 4)
        browseWin.mainloop()