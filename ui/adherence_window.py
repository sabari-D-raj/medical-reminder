import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from DATABASE import db
from analaysis import adherence

class adherence_window(tk.Toplevel):
    def __init__(self, parent, refresh_callback, db_obj: db.database, analytics: adherence.AdherenceAnalytics):
        super().__init__(parent)
        self.db = db_obj
        self.analytics = analytics
        self.refresh_callback = refresh_callback
        self.title("Mark Medication Taken")
        self.geometry("400x300")
        
        tk.Label(self, text="Select Medicine", font=("Arial", 12)).pack(pady=10)
        self.db.cursor.execute("SELECT id, medicine_name FROM medicine")
        self.medicines = {row[0]: row[1] for row in self.db.cursor.fetchall()}
        
        if not self.medicines:
            tk.Label(self, text="No medicines found").pack()
            return
        self.medicine_var = tk.StringVar()
        self.medicine_combo = ttk.Combobox(self, textvariable=self.medicine_var, 
                                            values=list(self.medicines.values()), state="readonly")
        self.medicine_combo.pack(pady=5, padx=20, fill=tk.X)
        tk.Label(self, text="Mark as taken today?", font=("Arial", 11)).pack(pady=10)
        self.taken_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self, text="Taken", variable=self.taken_var).pack(pady=5)
        tk.Button(self, text="Save", command=self.save, bg="green", fg="white").pack(pady=15)
    
    def save(self):
        if not self.medicine_var.get():
            tk.messagebox.showwarning("Error", "Please select a medicine")
            return
        med_id = [k for k, v in self.medicines.items() if v == self.medicine_var.get()][0]
        taken = 1 if self.taken_var.get() else 0
        
        self.analytics.mark_taken(med_id, taken)
        self.refresh_callback()
        tk.messagebox.showinfo("Success", "Adherence recorded successfully!")
        self.destroy()
