import tkinter as tk
#from  tkinter import ttk
from DATABASE import db
class medicine_window(tk.Toplevel):
    def __init__(self,parent,refresh_callback):
            super().__init__(parent)
            self.db=db
            self.title("add medication")
            self.refresh_callback=refresh_callback
            self.geometry("450x450")
            tk.Label(self,text="Name").pack()
            self.name_entry=tk.Entry(self).pack()
            tk.Label(self,text="Dosage").pack()
            self.dosage_entry=tk.Entry(self).pack()
            tk.Label(self,text="Time").pack()
            self.time_entry=tk.Entry(self).pack()
            tk.Label(self,text="Time of repeation").pack()
            self.repation=tk.Entry(self).pack()
            tk.Button(self,text="save",command=self.save).pack()
    def save(self):
          self.db.execute("""INSERT INTO medicine ( medicine_name,dosage,time,how many times a day) VALUES (?,?,?,?)  """,
                          (self.name_entry.get(),
                           self.dosage_entry.get(),
                           self.time_entry.get(),
                           self.repation.get())
                          )
          self.refresh_callback()
db.conn.commit()