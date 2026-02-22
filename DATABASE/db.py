import sqlite3

class database:
    def __init__(self,name="medications.db"):
        self.conn= sqlite3.connect(name)
        self.cursor=self.conn.cursor()
    def table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS medicine (
                                id INTEGER PRIMARY KEY AUTOINCREMENT    ,
                             medicine_name TEXT,
                            dosage TEXT,
                            time TEXT,
                            how_many_times_a_day TEXT
                            )""")
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Adherence (
                            
                            id INTEGER PRIMARY KEY AUTOIMCREMENT,
                            med_id INTEGER,
                            date TEXT,
                            taken INTEGER
                            )""")
        
        self.conn.commit()
