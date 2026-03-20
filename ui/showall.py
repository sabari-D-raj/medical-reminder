import tkinter as tk
from ui import medice
from ui import dashboard
from DATABASE import db
from analaysis import adherence
class main_window(tk.Frame):
    def __init__(self,root:tk.Tk,analytics:adherence.AdherenceAnalytics,db:db.database):
                super().__init__(root)
                self.db=db
                self.analytics=analytics
                tk.Label(self,text="MEDICINE REMINDER " ,font=('Arial',20))
                self.listbox=tk.Listbox(self)
                self.listbox.pack(padx=20)
                self.button=tk.Button(text="+add-medicine",command=self.addmed)
                self.dash=dashboard(self,analytics.overall_adherence())

    def refresh_list(self):
            self.listbox.delete(0,tk.END)
            self.db.cursor.execute("SELECT medicine_name,dosage,times_a_day FROM medicine" )
            for med in self.db.cursor.fetchall():
                    self.listbox.insert(tk.END,f"{med[0]}-{med[1]}-{med[2]}")
            self.dash.refresh()

    def addmed(self):
            medice(self,self.db,self.refresh_list)



                
                