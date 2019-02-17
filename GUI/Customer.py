from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import LoginWindow

class Customer:
    def __init__ (self, db):
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
        browse ()
    def switchToUpdate (self, _window):
        _window.destroy ()
        updateInfo ()
    def updateInfo (self):
        # TODO
        basic ()
    def basic (self):
        win = Tk ()
        win.title ("Welcome")
        win.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (win))  # handle window closing
        Button(win, text= 'Browse Products', command= lambda: switchToBrowse (win)).grid(row=1, column = 0, sticky=W)
        Button(win, text= 'Update your info', command= lambda: switchToUpdate (win)).grid(row=2, column = 0, sticky=W)
        Button (win, text = 'Back to Login', command = lambda : switchToLogin (win)).grid (row = 3, column = 0, sticky = W)
        win.mainloop ()
    def browse (self):
        browse = Tk ()
        browse.title ("Browse Products")
        browse.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (browse))  # handle window closing
        Label(browse, text = "Enter product name").grid (row = 0, column = 0, sticky = W)

        prodText = StringVar()

        Entry(browse, textvariable=prodText).grid (row = 0, column = 1, sticky = W)
        Button(browse, text= 'Search', command= lambda: populateProducts (prodText.get ())).grid(row=0, column = 2, sticky=W)
        Button (browse, text = 'Switch to Login', command = lambda: self.switchToLogin (browse)).grid (row = 9, sticky = W, pady = 4)
        browse.mainloop()