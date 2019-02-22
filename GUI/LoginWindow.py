from tkinter import *
from tkinter import messagebox
import Seller 
import SignUp

class LoginWindow:
    def __init__ (self, db):
        self.db = db
        self.loginWin()
    def on_closing(self, _window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()
    def loginWin (self):
        def enter (usr, supp, ship, output, username, password):
            cnt = usr.get () + supp.get () + ship.get ()
            strng = ""
            if (cnt == 0):
                strng = "You haven't checked any of the check box\n"
                output.delete (0.0, END)
                output.insert (END, strng)
            elif (cnt > 1):
                strng = "You must check exactly one tick box\n"
                output.delete (0.0, END)
                output.insert (END, strng)
            else:
                if (supp.get () == 1 and self.db.validate (username, password, "SUP")):
                    log.destroy ()
                    Supplier.Supplier (self.db, username)
        def openSign (log):
            log.destroy ()
            SignUp.SignUp (self.db)
        log = Tk()
        log.title("Login")
        log.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (log))  # handle window closing
        output = Text (log, height = 1, width = 40, wrap = WORD, bg = "white")
        output.grid (row = 3, column = 1)
        Label(log, text = "Username").grid (row = 0, column = 0, sticky = W)
        Label(log, text = "Password").grid (row = 1, column = 0, sticky = W)
        userText = StringVar()
        passText = StringVar ()
        Entry(log, textvariable=userText).grid (row = 0, column = 1, sticky = W)
        Entry(log, textvariable=passText, show = "*").grid (row = 1, column = 1, sticky = W)
        usr = IntVar ()
        supp = IntVar ()
        ship = IntVar ()
        Checkbutton(log, text="User", variable=usr).grid(row=2, column = 0, sticky=W)
        Checkbutton(log, text="Supplier", variable=supp).grid(row=2, column = 1, sticky=W)
        Checkbutton(log, text="Shipper", variable=ship).grid(row=2, column = 2, sticky=W)
        Button(log, text= 'Enter', command= lambda: enter(usr, supp, ship, output, userText.get (), passText.get ())).grid(row=3, sticky=W, pady=4)
        Button (log, text = "SignUp", command = lambda: openSign (log)).grid (row = 4, sticky = W, pady = 4)
        log.mainloop()