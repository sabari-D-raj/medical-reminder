import tkinter as tk
from ui import medice
from ui import dashboard
from DATABASE import db
class main_window(tk.Frame):
    def __init__(self,root,analytics):
                super().__init__(root)
                
                