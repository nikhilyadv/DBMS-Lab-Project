class supplier:
    def on_closing(_window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()
    supp = Tk()
    supp.title("Supplier")
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
    
def loginWindow ():
    def enter (usr, supp, ship, output):
        cnt = usr.get () + supp.get () + ship.get ()
        strng = ""
        if (cnt == 0):
            strng = "You haven't checked any of the check box\n"
        elif (cnt > 1):
            strng = "You must check exactly one tick box\n"
        output.delete (0.0, END)
        output.insert (END, strng)
    def openSign (log):
        log.destroy ()
        signUp ()
    log = Tk()
    log.title("Login")
    log.protocol("WM_DELETE_WINDOW", lambda: on_closing (log))  # handle window closing
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
    Button(log, text= 'Enter', command= lambda: enter(usr, supp, ship, output)).grid(row=3, sticky=W, pady=4)
    Button (log, text = "SignUp", command = lambda: openSign (log)).grid (row = 4, sticky = W, pady = 4)
    log.mainloop()
loginWindow ()