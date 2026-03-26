import tkinter as tk
from ui import medice
from ui.adherence_window import adherence_window
from ui.dashboard import dashboard
from ui.analytics_window import analytics_window
from ui.side_effects_window import side_effects_window
from ui.interactions_window import interactions_window
from ui.doctor_notes_window import doctor_notes_window
from ui.refill_reminders_window import refill_reminders_window
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
        
                button_frame1 = tk.Frame(self)
                button_frame1.pack(pady=10)
                tk.Button(button_frame1,text="+Add Medicine",command=self.addmed).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame1,text="Mark Taken",command=self.mark_adherence).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame1,text="Delete",command=self.delete).pack(side=tk.LEFT, padx=5)
        
                button_frame2 = tk.Frame(self)
                button_frame2.pack(pady=10)
                tk.Button(button_frame2,text="📊 Analytics",command=self.open_analytics).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame2,text="⚠️ Side Effects",command=self.open_side_effects).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame2,text="💊 Interactions",command=self.open_interactions).pack(side=tk.LEFT, padx=5)
                

                button_frame3 = tk.Frame(self)
                button_frame3.pack(pady=10)
                tk.Button(button_frame3,text="📝 Doctor Notes",command=self.open_doctor_notes).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame3,text="🔔 Refill Reminders",command=self.open_refill).pack(side=tk.LEFT, padx=5)
                
                self.dash=dashboard(self,analytics)
                self.dash.pack(pady=10)


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
    
    def open_analytics(self):
        analytics_win = analytics_window(self, self.db, self.analytics)
        analytics_win.grab_set()
    
    def open_side_effects(self):
        effects_win = side_effects_window(self, self.db)
        effects_win.grab_set()
    
    def open_interactions(self):
        interactions_win = interactions_window(self, self.db)
        interactions_win.grab_set()
    
    def open_doctor_notes(self):
        notes_win = doctor_notes_window(self, self.db)
        notes_win.grab_set()
    
    def open_refill(self):
        refill_win = refill_reminders_window(self, self.db)
        refill_win.grab_set()


                
                