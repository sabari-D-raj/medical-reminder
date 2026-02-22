import tkinter as tk

class dashboard(tk.Frame):
    def __init__(self,parent,adherence):
        super().__init__(parent)
        self.tk.title("Dashbord")
        self.geometry("400x400")
        self.analaysis=adherence
        

    