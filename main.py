from analaysis import adherence
from ui import showall
from DATABASE import db
import tkinter as tk
def main():
    root=tk.Tk()
    root.title("medicine reminder")
    root.geometry("500x500")
    database=db.database()
    analytics=adherence.AdherenceAnalytics(database)
    app=showall.main_window(root,analytics,database)
    app.pack()
    app.refresh_list()
    root.mainloop()
if __name__=="__main__":
    main()

