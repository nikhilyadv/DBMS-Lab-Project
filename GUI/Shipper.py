from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import requests
import datetime
import LoginWindow



class Shipper:
    def __init__ (self, db, username):
        self.db = db
        self.shipper_id = username
        self.basic ()


    
    def on_closing(self, _window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()


    def switchToShipmentsDuration (self, _window):
        _window.destroy ()
        self.shipmentsDuration()


    def switchToLogin (self, _window):
        _window.destroy ()
        LoginWindow.LoginWindow ()

    def switchToBasic(self,_window):
        _window.destroy()
        self.basic()
    
    def switchToUpdate (self, _window):
        _window.destroy ()
        self.updateInfo ()

    def switchToLatestNShipments (self, _window):
        _window.destroy ()
        self.latestNShipments()

    def shipmentsDuration(self):
        win = Tk ()
        win.title ("See Past Shipments")
        win.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (win)) 

        Label(win, text = "Start Year").grid (row = 0, column = 0, sticky = W)
        Label(win, text = "Start Month").grid (row = 0, column = 2, sticky = W)
        Label(win, text = "Start Day").grid (row = 0, column = 4, sticky = W)
        Label(win, text = "End Year").grid (row = 1, column = 0, sticky = W)
        Label(win, text = "End Month").grid (row = 1, column = 2, sticky = W)
        Label(win, text = "End Day").grid (row = 1, column = 4, sticky = W)

        month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        year = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
        day = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]  


        startYear = StringVar ()
        startYear.set(year[0])
        startMonth = StringVar ()
        startMonth.set(month[0])
        startDay = StringVar ()
        startDay.set(day[0])
        endYear = StringVar ()
        endYear.set(year[0])
        endMonth = StringVar ()
        endMonth.set(month[0])
        endDay = StringVar ()
        endDay.set(day[0])

        OptionMenu(win, startYear, *year).grid(row = 0, column = 1, sticky = W)
        OptionMenu(win, startMonth, *month).grid(row = 0, column = 3, sticky = W)
        OptionMenu(win, startDay, *day).grid(row = 0, column = 5, sticky = W)
        OptionMenu(win, endYear, *year).grid(row = 1, column = 1, sticky = W)
        OptionMenu(win, endMonth, *month).grid(row = 1, column = 3, sticky = W)
        OptionMenu(win, endDay, *day).grid(row = 1, column = 5, sticky = W)

        Button (win, text = 'Switch to Login', command = lambda: self.switchToLogin (win)).grid (row = 21, sticky = W, pady = 4)
        output = Text (win, height = 1, width = 150, wrap = WORD, bg = "white")
        output.grid (row = 21, column = 1, columnspan = 1000)

        ttk.Style().configure('PViewStyle.Treeview', rowheight=60)
        plist = ttk.Treeview (win, style='PViewStyle.Treeview')
        scbVDirSel =Scrollbar(win, orient=VERTICAL, command=plist.yview)
        scbVDirSel.grid(row=2, column=100, rowspan=50, sticky=NS, in_=win)
        plist.configure(yscrollcommand=scbVDirSel.set) 

        def validDate(year, month, day):
            correctDate = None
            try:
                newDate = datetime.datetime(year, month, day)
                correctDate = True
            except ValueError:
                correctDate = False
            return correctDate

        def populate (years, months, days, yeare, monthe, daye, plist):
            strng = ""
            if (validDate (int(years), int(months), int(days)) and validDate (int(yeare), int(monthe), int(daye))):
                rows = self.db.seeShipmentsBetweenDuration(years, months, days, yeare, monthe, daye)
                plist.delete (*plist.get_children ())
                for row in rows:
                    plist.insert ('', 'end', values = row)
                strng = "Done!"
            else:
                strng = "Entered date is not valid!"

            output.delete (0.0, END)
            output.insert (END, strng)                    
        plist['columns'] = ('index_', 'shipper_id', 'tracking_id', 'date_')
        plist.heading ('index_', text = 'Index')
        plist.heading ('shipper_id', text = 'Shipper ID')
        plist.heading ('tracking_id', text = 'Tracking ID')
        plist.heading ('date_', text = 'Date')
        plist['show'] = 'headings'
        plist.grid(row = 2, column = 0, rowspan = 18, columnspan = 100)
        Button(win, text= 'Search', command= lambda: populate (startYear.get(), startMonth.get(), startDay.get(), endYear.get(), endMonth.get(), endDay.get(), plist)).grid(row=1, column=7, sticky=W)
        win.mainloop()
    
    def updateInfo (self):
        win = Tk ()
        win.title ("Update Info (You must enter your previous password and in case you don't want to change any of the respective info then leave that field empty or as it is)")
        win.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (win))  # handle window closing
        output = Text (win, height = 1, width = 60, wrap = WORD, bg = "white")
        output.grid (row = 7, column = 1)
        Label(win, text = "Previous Password").grid (row = 0, column = 0, sticky = W)
        Label(win, text = "New Password (can be same as old one) - leave this field empty if you don't want to change your password").grid (row = 1, column = 0, sticky = W)
        Label(win, text = "Repeat New Password - again, leave this field empty if you don't want wish to change your password").grid (row = 2, column = 0, sticky = W)
        Label(win, text = "Name").grid (row = 3, column = 0, sticky = W)
        Label(win, text = "Head Quarters").grid (row = 4, column = 0, sticky = W)
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
                    self.db.shipperUpdateInfo(self.shipper_id, npassword, name, add, phone, email)
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



    def latestNShipments(self):
        win = Tk ()
        win.title ("See latest N Shipments")
        win.protocol("WM_DELETE_WINDOW", lambda: self.switchToBasic (win)) 

        Label(win, text = "N: (min 1)").grid (row = 0, column = 0, sticky = W)

        n = IntVar ()
        Entry(win, textvariable=n).grid (row = 0, column = 1, sticky = W)

        Button (win, text = 'Switch to Login', command = lambda: self.switchToLogin (win)).grid (row = 21, sticky = W, pady = 4)
        output = Text (win, height = 1, width = 150, wrap = WORD, bg = "white")
        output.grid (row = 21, column = 1, columnspan = 1000)

        ttk.Style().configure('PViewStyle.Treeview', rowheight=60)
        plist = ttk.Treeview (win, style='PViewStyle.Treeview')
        scbVDirSel =Scrollbar(win, orient=VERTICAL, command=plist.yview)
        scbVDirSel.grid(row=2, column=100, rowspan=50, sticky=NS, in_=win)
        plist.configure(yscrollcommand=scbVDirSel.set) 

        def populate (n, plist):
            strng = ""
            if (n > 0):
                rows = self.db.seeLatestNShipments(n)
                plist.delete (*plist.get_children ())
                for row in rows:
                    plist.insert ('', 'end', values = row)
                strng = "Done!"
            else:
                strng = "Entered N is not valid!"

            output.delete (0.0, END)
            output.insert (END, strng)                    

        plist['columns'] = ('index_', 'shipper_id', 'tracking_id', 'date_')
        plist.heading ('index_', text = 'Index')
        plist.heading ('shipper_id', text = 'Shipper ID')
        plist.heading ('tracking_id', text = 'Tracking ID')
        plist.heading ('date_', text = 'Date')
        plist['show'] = 'headings'
        plist.grid(row = 2, column = 0, rowspan = 18, columnspan = 100)
        Button(win, text= 'Search', command= lambda: populate (n.get(), plist)).grid(row=1, column=7, sticky=W)
        win.mainloop()



    def basic(self):
        ship = Tk()
        ship.title("Welcome Shipper")
        ship.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (ship))
        Button(ship, text= 'Update Your Info', command= lambda: self.switchToUpdate (ship)).grid(row=3, column=0)
        Button(ship, text= 'See Your Past Shippments Between Some Duration', command= lambda: self.switchToShipmentsDuration (ship)).grid(row=4, column=0)
        Button(ship, text= 'See Your Latest N Shipments', command= lambda: self.switchToLatestNShipments (ship)).grid(row=5, column=0)
        ship.mainloop()