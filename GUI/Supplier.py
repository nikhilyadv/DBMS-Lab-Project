from tkinter import *
from tkinter import messagebox

class Supplier:
    def __init__ (self, db, username):
        self.db = db
        self.supplier_id = username
        self.window ()

    def on_closing(self, _window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            _window.destroy()
    
    def existprod (self):
        prod = Tk()
        prod.title("Update Product")
        prod.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (prod))

        def add(product_id, supplier_id, price, total_stock) :
            self.db.updateproduct (product_id, supplier_id, price, total_stock)
            prod.destroy ()
            self.window ()
        
        Label(prod, text = "Product Id").grid (row = 0, column = 0, sticky = W)
        Label(prod, text = "Price").grid (row = 0, column = 2, sticky = W)
        Label(prod, text = "Quantity").grid (row = 0, column = 4, sticky = W)

        product_id = StringVar()
        supplier_id = self.supplier_id
        price = StringVar()
        total_stock = IntVar()

        Entry(prod, textvariable = product_id).grid (row = 0, column = 1, sticky = W)
        Entry(prod, textvariable = price).grid (row = 0, column = 3, sticky = W)
        Entry(prod, textvariable = total_stock).grid (row = 0, column = 5, sticky = W)

        Button(prod, text = "Update Changes", command= lambda: add(product_id.get (), supplier_id, price.get (), total_stock.get ())).grid (row = 1, column = 0, sticky = W)
        prod.mainloop()
    
    def newprod (self):
        prod = Tk()
        prod.title("Add Product")
        prod.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (prod))

        def add(product_id, supplier_id, price, total_stock, description):
            print (product_id, supplier_id, price, total_stock, description, "\n")
            self.db.addproduct (product_id, supplier_id, price, total_stock, description)
            prod.destroy ()
            self.window ()
        
        Label(prod, text = "Product Id").grid (row = 0, column = 0, sticky = W)
        Label(prod, text = "Price").grid (row = 0, column = 2, sticky = W)
        Label(prod, text = "Quantity").grid (row = 0, column = 4, sticky = W)
        Label(prod, text = "Description").grid (row = 1, column = 0, sticky = W)

        product_id = StringVar()
        supplier_id = self.supplier_id
        price = StringVar()
        total_stock = IntVar()
        description = StringVar()

        Entry(prod, textvariable = product_id).grid (row = 0, column = 1, sticky = W)
        Entry(prod, textvariable = price).grid (row = 0, column = 3, sticky = W)
        Entry(prod, textvariable = total_stock).grid (row = 0, column = 5, sticky = W)
        Entry(prod, textvariable = description).grid (row = 1, column = 1, sticky = W)
        print (product_id.get (), supplier_id, price.get (), total_stock.get (), description.get (), "\n")
        Button(prod, text = "Add Product", command= lambda: add(product_id.get (), supplier_id, price.get (), total_stock.get (), description.get ())).grid (row = 2, column = 0, sticky = W)
        prod.mainloop()
    
    def window(self):
        supp = Tk()
        supp.title("Welcome Supplier")
        supp.protocol("WM_DELETE_WINDOW", lambda: self.on_closing (supp))
        def addnewprods ():
            supp.destroy ()
            self.newprod ()
        def addexistingprods ():
            supp.destroy ()
            self.existprod ()
        Button(supp, text= 'Add new products', command= addnewprods).grid(row=3, column=2)
        Button(supp, text= 'Add existing products', command= addexistingprods).grid(row=3, column=4)
        supp.mainloop()
