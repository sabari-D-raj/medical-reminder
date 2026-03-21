import tkinter as tk
from ui import medice
from ui.adherence_window import adherence_window
from ui.dashboard import dashboard
from DATABASE import db
from analaysis import adherence
class main_window(tk.Frame):
    dist={}
    def __init__(self,root:tk.Tk,analytics:adherence.AdherenceAnalytics,db:db.database):
                super().__init__(root)
                self.db=db
                self.analytics=analytics
                tk.Label(self,text="MEDICINE TRACKER " ,font=('Arial',20)).pack()
                self.listbox=tk.Listbox(self,width=80,font=("Arial",15))
                self.listbox.pack(padx=20)
                self.button=tk.Button(self,text="+add-medicine",command=self.addmed)
                self.button.pack(pady=10)
                self.dash=dashboard(self,analytics)
                self.dash.pack(pady=10)
                tk.Button(self,text="Mark Medicine Taken",command=self.mark_adherence).pack(pady=10)
                tk.Button(self,text="Delete",command=self.delete).pack(pady=15)


    def refresh_list(self):
            self.listbox.delete(0,tk.END)
            self.db.cursor.execute("SELECT id,medicine_name,dosage,times_a_day,days_to_take FROM medicine" )
            self.dist={}
            id=0
            for med in self.db.cursor.fetchall():
                    self.dist[id]=med[0]
                    self.listbox.insert(tk.END,f"{med[1]}-{med[2]}-{med[3]}-{med[4]}")
                    id += 1
            self.dash.refresh()

    def addmed(self):
        med_window=medice.medicine_window(self,self.refresh_list,self.db)
        med_window.grab_set()
    def mark_adherence(self):
        adherence_win=adherence_window(self,self.refresh_list,self.db,self.analytics)
        adherence_win.grab_set()
    def delete(self):
        selected=self.listbox.curselection()
        
        if selected:
            med_id=self.dist.get(selected[0])
            self.db.cursor.execute("DELETE FROM medicine WHERE id=?", (med_id,))
            self.refresh_list()
            self.db.conn.commit()


                
                