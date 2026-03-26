import tkinter as tk
from DATABASE import db
class medicine_window(tk.Toplevel):
    def __init__(self,parent,refresh_callback,db:db.database):
            super().__init__(parent)
            self.db=db
            self.title("add medication")
            self.refresh_callback=refresh_callback
            self.geometry("450x550")
            tk.Label(self,text="Name").pack()
            self.name_entry=tk.Entry(self)
            self.name_entry.pack()
            tk.Label(self,text="Dosage").pack()
            self.dosage_entry=tk.Entry(self)
            self.dosage_entry.pack()
            
            tk.Label(self,text="Time").pack()
            self.time_entry=tk.Entry(self)
            self.time_entry.pack()
            tk.Label(self,text="Time of repeation").pack()
            self.repation=tk.Entry(self)
            self.repation.pack()
            tk.Label(self,text="days to take").pack()
            self.days=tk.Entry(self)
            self.days.pack()
            tk.Label(self,text="Stock Quantity (pills/tablets)").pack()
            self.stock_entry=tk.Entry(self)
            self.stock_entry.pack()
            tk.Button(self,text="save",command=self.save).pack(pady=10)
            

    def save(self):
          self.db.cursor.execute("""INSERT INTO medicine ( medicine_name,dosage,time,times_a_day,days_to_take,stock_quantity ) VALUES (?,?,?,?,?,?)  """,
                          (self.name_entry.get(),
                           self.dosage_entry.get(),
                           self.time_entry.get(),
                           self.repation.get(),
                           self.days.get(),
                           int(self.stock_entry.get()) if self.stock_entry.get() else 0)
                          )
          self.refresh_callback()
          self.db.conn.commit()
          self.destroy()
