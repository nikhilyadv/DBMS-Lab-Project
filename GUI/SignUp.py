from tkinter import *
from tkinter import messagebox

class SignUp (db):
    def on_closing(_window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()
    def window1():
        win = Tk()
        win.title("Sign Up")
        win.protocol("WM_DELETE_WINDOW", lambda: on_closing (sign))  # handle window closing
        outputAbove = Text (win, height = 1, width = 60, wrap = WORD, bg = "white")
        outputAbove.grid (row = 0, column = 0)
        outputAbove.insert (END, "Please select your role:")
        outputBelow = Text (win, height = 1, width = 60, wrap = WORD, bg = "white")
        outputBelow.grid (row = 2, column = 0)
        usr = IntVar ()
        supp = IntVar ()
        ship = IntVar ()
        Checkbutton(win, text="User", variable=usr).grid(row=1, column = 0, sticky=W)
        Checkbutton(win, text="Supplier", variable=supp).grid(row=1, column = 1, sticky=W)
        Checkbutton(win, text="Shipper", variable=ship).grid(row=1, column = 2, sticky=W)
        def reg1 ():
            cnt = usr.get () + supp.get () + ship.get ()
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
                if (supp.get () == 1):
                    supplierSign ()
                elif (usr.get () == 1):
                    userSign ()
                else:
                    shipperSign ()
        Button(win, text= 'Proceed', command= reg1).grid(row=3, sticky=W, pady=4)
        win.mainloop()
    def userSign ():
        sign = Tk ()
        sign.title ("Sign up")
        sign.protocol("WM_DELETE_WINDOW", lambda: on_closing (sign))  # handle window closing
        output = Text (sign, height = 1, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 4, column = 1)
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
        Entry(sign, textvariable=name).grid (row = 0, column = 1, sticky = W)
        Entry(sign, textvariable=add).grid (row = 0, column = 1, sticky = W)
        Entry(sign, textvariable=phone).grid (row = 0, column = 1, sticky = W)
        Entry(sign, textvariable=userText).grid (row = 0, column = 1, sticky = W)
        Entry(sign, textvariable=userText).grid (row = 0, column = 1, sticky = W)
        usr = IntVar ()
        supp = IntVar ()
        ship = IntVar ()
        Checkbutton(sign, text="User", variable=usr).grid(row=3, column = 0, sticky=W)
        Checkbutton(sign, text="Supplier", variable=supp).grid(row=3, column = 1, sticky=W)
        Checkbutton(sign, text="Shipper", variable=ship).grid(row=3, column = 2, sticky=W)
        Button(sign, text= 'Register', command= lambda: reg(usr, supp, ship, output, userText.get (), passText.get (), repPassText.get ())).grid(row=4, sticky=W, pady=4)
        Button (sign, text = 'Switch to Login', command = lambda: getLogin (sign)).grid (row = 5, sticky = W, pady = 4)
        sign.mainloop()
    def signUp ():
        def getLogin (sign):
            sign.destroy ()
            loginWindow ()
        def reg (usr, supp, ship, output, username, password, ppasword):
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
            elif (password != ppasword): 
                strng = "Your passwords don't match\n"
                output.delete (0.0, END)
                output.insert (END, strng)
            else:   # must add this to the database
                strng = "Successfully registered, you may now proceed to login window"
                output.delete (0.0, END)
                output.insert (END, strng)
                db.addUser (username, password)
        sign = Tk()
        sign.title("Sign Up")
        sign.protocol("WM_DELETE_WINDOW", lambda: on_closing (sign))  # handle window closing
        output = Text (sign, height = 1, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 4, column = 1)
        Label(sign, text = "Username").grid (row = 0, column = 0, sticky = W)
        Label(sign, text = "Password").grid (row = 1, column = 0, sticky = W)
        Label(sign, text = "Repeat Password").grid (row = 2, column = 0, sticky = W)
        userText = StringVar()
        passText = StringVar ()
        repPassText = StringVar ()
        Entry(sign, textvariable=userText).grid (row = 0, column = 1, sticky = W)
        Entry(sign, textvariable=passText, show = "*").grid (row = 1, column = 1, sticky = W)
        Entry(sign, textvariable=repPassText, show = "*").grid (row = 2, column = 1, sticky = W)
        usr = IntVar ()
        supp = IntVar ()
        ship = IntVar ()
        Checkbutton(sign, text="User", variable=usr).grid(row=3, column = 0, sticky=W)
        Checkbutton(sign, text="Supplier", variable=supp).grid(row=3, column = 1, sticky=W)
        Checkbutton(sign, text="Shipper", variable=ship).grid(row=3, column = 2, sticky=W)
        Button(sign, text= 'Register', command= lambda: reg(usr, supp, ship, output, userText.get (), passText.get (), repPassText.get ())).grid(row=4, sticky=W, pady=4)
        Button (sign, text = 'Switch to Login', command = lambda: getLogin (sign)).grid (row = 5, sticky = W, pady = 4)
        sign.mainloop()