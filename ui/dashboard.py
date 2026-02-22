import tkinter as tk
from analaysis import adherence
class dashboard(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.analaysis=adherence
        self.label=tk.Label(self,text="overall adhrence 0%").pack()
        self.refresh()
        def refresh(self):
            percent=self.analaysis.overall_adherence()
            self.label.config(text=f"overall adherence: {percent}").pack()
            
            