from tkinter import *
from tkinter import messagebox
from Shipper import Shipper
from Seller import Seller 
from Customer import Customer
import SignUp

class LoginWindow:
    def __init__ (self, db):
        self.db = db
        self.loginWin()
    def on_closing(self, _window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()
    def loginWin (self):
        def enter (output, username, password):
            if (self.db.validate (username, password)):
                log.destroy ()
                role = self.db.getrole (username, password)
                self.db.loginUser (username, password, role)
                if role == "customer":
                    Customer (self.db, username)
                elif role == "seller":
                    Seller (self.db, username)
                else:
                    Shipper (self.db, username)
            else:
                strng = "Invalid credentials\n"
                output.delete (0.0, END)
                output.insert (END, strng)

        def openSign (log):
            log.destroy ()
            SignUp.SignUp (self.db)
        log = Tk()
        log.title("Login")
        log.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (log)) 
        output = Text (log, height = 1, width = 40, wrap = WORD, bg = "white")
        output.grid (row = 3, column = 1)
        Label(log, text = "Username").grid (row = 0, column = 0, sticky = W)
        Label(log, text = "Password").grid (row = 1, column = 0, sticky = W)
        userText = StringVar()
        passText = StringVar ()
        Entry(log, textvariable=userText).grid (row = 0, column = 1, sticky = W)
        Entry(log, textvariable=passText, show = "*").grid (row = 1, column = 1, sticky = W)
        Button(log, text= 'Enter', command= lambda: enter(output, userText.get (), passText.get ())).grid(row=3, sticky=W, pady=4)
        Button (log, text = "SignUp", command = lambda: openSign (log)).grid (row = 4, sticky = W, pady = 4)
        log.mainloop()