import tkinter as tk
from  tkinter import ttk
class medicine_window(tk.Toplevel):
    def __init__(self):
            self.title="add medication"
            self.geometry="450x450"
            tk.Label(self,text="Name").pack()
            self.name_entry=tk.Entry(self).pack()
            tk.Label(self,text="Dosage").pack()
            self.dosage_entry=tk.Entry(self).pack()
            tk.Label(self,text="Time").pack()
            self.time_entry=tk.Entry(self).pack()
            tk.Label(self,text="Time of repeation").pack()
            self.repation=tk.Entry(self).pack()
    def save(self,db):
          pass
            