import sqlite3

class database:
    def __init__(self,name="medication.db"):
        self.conn= sqlite3.connect(name)
        self.cursor=self.conn.cursor()
    def table(self):
        self.cursor.execute("""CREATE TABLE medicine (
                                id INTEGER PRIMARY KEY AUTOINCREMENT    ,
                             medicine name TEXT,
                            dosage TEXT,
                            time TEXT,
                            how many times a day TEXT
                            )""")
        
        self.conn.commit()
table=database()
