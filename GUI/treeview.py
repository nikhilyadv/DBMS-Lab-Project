from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk


browseWin = Tk ()
plist = ttk.Treeview (browseWin)
plist['columns'] = ('el', 'mn')
v = PhotoImage(file = '/home/sourabh/Documents/Github/DBMS-Lab-Project/TkinterReference/small.png')
plist.heading('#0', text = 'mewo')
plist.heading('el', text = 'om')
plist.heading('mn', text = 'lala')
# plist['show'] = 'headings'
plist.pack ()
plist.insert ('', 'end', values = ('sss', 'smd'), image = v)
browseWin.mainloop()