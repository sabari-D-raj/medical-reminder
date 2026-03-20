import tkinter as tk
from analaysis import adherence
class dashboard(tk.Frame):
    def __init__(self, parent, analytics:adherence.AdherenceAnalytics):
        super().__init__(parent)
        self.analytics = analytics
        self.label = tk.Label(self, text="overall adherence 0%")
        self.label.pack()
        self.refresh()
    def refresh(self):
        percent = self.analytics.overall_adherence()
        self.label.config(text=f"overall adherence: {percent}%")
            
            