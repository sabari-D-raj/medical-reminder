import sqlite3
class database:
    def __init__(self,name="medications.db"):
        self.conn= sqlite3.connect(name)
        self.cursor=self.conn.cursor()
        self.table()

    def table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS medicine (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                             medicine_name TEXT NOT NULL,
                            dosage TEXT NOT NULL,
                            time  DATETIME DEFAULT CURRENT_TIMESTAMP,
                            times_a_day INTEGER NOT NULL,
                            days_to_take INTEGER NOT NULL
                            )""")
        
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Adherence (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            med_id INTEGER,
                            date TEXT,
                            taken INTEGER,
                            FOREIGN KEY (med_id) REFERENCES medicine(id)
                            ON UPDATE CASCADE 
                            ON DELETE CASCADE
                            )""")
        
        self.conn.commit()
