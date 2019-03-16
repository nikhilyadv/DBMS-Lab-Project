from tkinter import *
from tkinter import messagebox
import LoginWindow

class SignUp:
    def __init__ (self, db):
        self.db = db
        self.window1()
    def on_closing(self, _window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()
    def switchToLogin (self, _window):
        _window.destroy ()
        LoginWindow.LoginWindow ()
    def window1(self):
        win = Tk()
        win.title("Sign Up")
        win.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (win))  # handle window closing
        outputAbove = Text (win, height = 1, width = 60, wrap = WORD, bg = "white")
        outputAbove.grid (row = 0, column = 0)
        outputAbove.insert (END, "Please select your role:")
        outputBelow = Text (win, height = 1, width = 60, wrap = WORD, bg = "white")
        outputBelow.grid (row = 2, column = 0)
        usr = IntVar ()
        sell = IntVar ()
        ship = IntVar ()
        Checkbutton(win, text="Customer", variable=usr).grid(row=1, column = 0, sticky=W)
        Checkbutton(win, text="Seller", variable=sell).grid(row=1, column = 1, sticky=W)
        Checkbutton(win, text="Shipper", variable=ship).grid(row=1, column = 2, sticky=W)
        def reg1 ():
            cnt = usr.get () + sell.get () + ship.get ()
            strng = ""
            if (cnt == 0):
                strng = "Error: You haven't checked any of the check box\n"
                outputBelow.delete (0.0, END)
                outputBelow.insert (END, strng)
            elif (cnt > 1):
                strng = "Error: You must check exactly one tick box\n"
                outputBelow.delete (0.0, END)
                outputBelow.insert (END, strng)
            else:   # must add this to the database
                win.destroy ()
                if (sell.get () == 1):
                    self.sellerSign ()
                elif (usr.get () == 1):
                    self.customerSign ()
                else:
                    self.shipperSign ()
        Button(win, text= 'Proceed', command= reg1).grid(row=3, sticky=W, pady=4)
        win.mainloop()
    def customerSign (self):
        sign = Tk ()
        sign.title ("Sign up")
        sign.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (sign))  # handle window closing
        output = Text (sign, height = 1, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 7, column = 1)
        Label(sign, text = "Username").grid (row = 0, column = 0, sticky = W)
        Label(sign, text = "Password").grid (row = 1, column = 0, sticky = W)
        Label(sign, text = "Repeat Password").grid (row = 2, column = 0, sticky = W)
        Label(sign, text = "Name").grid (row = 3, column = 0, sticky = W)
        Label(sign, text = "Address").grid (row = 4, column = 0, sticky = W)
        Label(sign, text = "Phone number").grid (row = 5, column = 0, sticky = W)
        Label(sign, text = "email-id").grid (row = 6, column = 0, sticky = W)

        userText = StringVar()
        passText = StringVar ()
        repPassText = StringVar ()
        name = StringVar ()
        add = StringVar ()
        phone = IntVar ()
        email = StringVar ()

        Entry(sign, textvariable=userText).grid (row = 0, column = 1, sticky = W)
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
        def check (username, password, ppassword, name, add, phone, email):
            strng = ""

            if (fine(username) and fine(password) and ppassword == password and fine(name) and fine(add) and fine(str(phone)) and fine(email)):
                if self.db.createUser(username, password, "customer", name, add, phone, email) == False:
                    strng = "User already exists!\n"
                else :
                    strng = "{} successfully inserted".format (username)
                output.delete(0.0, END)
                output.insert(END, strng)
            else:
                if (password != ppassword):
                    strng = "Your Passwords don't match!\n"
                elif (self.db.userExists (username)):
                    strng = "This username already exists!\n"
                else:
                    strng = "You have an entry missing!\n"
                output.delete (0.0, END)
                output.insert (END, strng)
        Button(sign, text= 'Register', command= lambda: check (userText.get (), passText.get (), repPassText.get (), name.get (), add.get (), phone.get (), email.get ())).grid(row=8, sticky=W, pady=4)
        Button (sign, text = 'Switch to Login', command = lambda: self.switchToLogin (sign)).grid (row = 9, sticky = W, pady = 4)
        sign.mainloop()

    def sellerSign (self):
        sign = Tk ()
        sign.title ("Sign up")
        sign.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (sign))  # handle window closing
        output = Text (sign, height = 1, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 7, column = 1)
        Label(sign, text = "Username").grid (row = 0, column = 0, sticky = W)
        Label(sign, text = "Password").grid (row = 1, column = 0, sticky = W)
        Label(sign, text = "Repeat Password").grid (row = 2, column = 0, sticky = W)
        Label(sign, text = "Name").grid (row = 3, column = 0, sticky = W)
        Label(sign, text = "Address").grid (row = 4, column = 0, sticky = W)
        Label(sign, text = "Phone number").grid (row = 5, column = 0, sticky = W)
        Label(sign, text = "email-id").grid (row = 6, column = 0, sticky = W)

        userText = StringVar()
        passText = StringVar ()
        repPassText = StringVar ()
        name = StringVar ()
        add = StringVar ()
        phone = IntVar ()
        email = StringVar ()

        Entry(sign, textvariable=userText).grid (row = 0, column = 1, sticky = W)
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
        def check (username, password, ppassword, name, add, phone, email):
            strng = ""

            if (fine(username) and fine(password) and ppassword == password and fine(name) and fine(add) and fine(str(phone)) and fine(email)):
                if self.db.createUser(username, password, "seller", name, add, phone, email) == False:
                    strng = "User already exists!\n"
                else :
                    strng = "{} successfully inserted".format (username)
                output.delete(0.0, END)
                output.insert(END, strng)
            else:
                if (password != ppassword):
                    strng = "Your Passwords don't match!\n"
                elif (self.db.userExists (username)):
                    strng = "This username already exists!\n"
                else:
                    strng = "You have an entry missing!\n"
                output.delete (0.0, END)
                output.insert (END, strng)
        Button(sign, text= 'Register', command= lambda: check (userText.get (), passText.get (), repPassText.get (), name.get (), add.get (), phone.get (), email.get ())).grid(row=8, sticky=W, pady=4)
        Button (sign, text = 'Switch to Login', command = lambda: self.switchToLogin (sign)).grid (row = 9, sticky = W, pady = 4)
        sign.mainloop()
   
    def shipperSign (self):
        sign = Tk ()
        sign.title ("Sign up")
        sign.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (sign))  # handle window closing
        output = Text (sign, height = 1, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 7, column = 1)
        Label(sign, text = "Username").grid (row = 0, column = 0, sticky = W)
        Label(sign, text = "Password").grid (row = 1, column = 0, sticky = W)
        Label(sign, text = "Repeat Password").grid (row = 2, column = 0, sticky = W)
        Label(sign, text = "Name").grid (row = 3, column = 0, sticky = W)
        Label(sign, text = "Address").grid (row = 4, column = 0, sticky = W)
        Label(sign, text = "Phone number").grid (row = 5, column = 0, sticky = W)
        Label(sign, text = "email-id").grid (row = 6, column = 0, sticky = W)

        userText = StringVar()
        passText = StringVar ()
        repPassText = StringVar ()
        name = StringVar ()
        add = StringVar ()
        phone = IntVar ()
        email = StringVar ()

        Entry(sign, textvariable=userText).grid (row = 0, column = 1, sticky = W)
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
        def check (username, password, ppassword, name, add, phone, email):
            strng = ""

            if (fine(username) and fine(password) and ppassword == password and fine(name) and fine(add) and fine(str(phone)) and fine(email)):
                if self.db.createUser(username, password, "shipper", name, add, phone, email) == False:
                    strng = "User already exists!\n"
                else :
                    strng = "{} successfully inserted".format (username)
                output.delete(0.0, END)
                output.insert(END, strng)
            else:
                if (password != ppassword):
                    strng = "Your Passwords don't match!\n"
                elif (self.db.userExists (username)):
                    strng = "This username already exists!\n"
                else:
                    strng = "You have an entry missing!\n"
                output.delete (0.0, END)
                output.insert (END, strng)
        Button(sign, text= 'Register', command= lambda: check (userText.get (), passText.get (), repPassText.get (), name.get (), add.get (), phone.get (), email.get ())).grid(row=8, sticky=W, pady=4)
        Button (sign, text = 'Switch to Login', command = lambda: self.switchToLogin (sign)).grid (row = 9, sticky = W, pady = 4)
        sign.mainloop()
 