class DB:
    def __init__ (self):
        self.conn = sql.connect (user = "root", password = "root", db = "delMe")
        self.cur = self.conn.cursor ()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS book (id INTEGER AUTO_INCREMENT PRIMARY KEY, title varchar(20), author varchar(20), isbn INTEGER)")
        self.conn.commit ()

    def __del__(self):  # destructor
        self.conn.close()  # close connection

    def view(self):
        self.cur.execute("SELECT * FROM book")
        rows = self.cur.fetchall()
        return rows

    def insert(self, title, author, isbn):
        print ("just checking {} {} {}".format(title, author, isbn))
        self.cur.execute("INSERT INTO book (title, author, isbn) VALUES (\"{}\",\"{}\",{})".format(title, author, isbn))
        self.conn.commit()
        self.view()

    def update(self, id, title, author, isbn):
        self.cur.execute("UPDATE book SET title={}, author={}, isbn={} WHERE id={}".format(title, author, isbn, id))
        self.view()

    def delete(self, id):
        self.cur.execute("DELETE FROM book WHERE id={}".format(id))
        self.conn.commit()
        self.view()

    def search(self, title="", author="", isbn=""):
        self.cur.execute("SELECT * FROM book WHERE title=\"{}\" OR author=\"{}\" OR isbn={}".format(title, author, isbn))
        rows = self.cur.fetchall()
        return rows
    def addUser (self, username, password):
        print ("Meow")