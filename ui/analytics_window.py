import tkinter as tk
from tkinter import ttk
from DATABASE import db
from analaysis import adherence

class analytics_window(tk.Toplevel):
    def __init__(self, parent, database: db.database, analytics: adherence.AdherenceAnalytics):
        super().__init__(parent)
        self.db = database
        self.analytics = analytics
        self.title("Analytics & Insights")
        self.geometry("800x600")
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_medicine_adherence_tab()
        
        self.create_trends_tab()
        
        self.create_missed_doses_tab()
        
        self.create_streaks_tab()

    def create_medicine_adherence_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Medicine Adherence")
        
        tk.Label(frame, text="Select Medicine:", font=("Arial", 12)).pack(pady=10)
        
        self.medicine_var = tk.StringVar()
        medicines = self.db.get_all_medicines()
        med_names = [f"{m[1]} ({m[2]})" for m in medicines]
        med_dict = {f"{m[1]} ({m[2]})": m[0] for m in medicines}
        
        combo = ttk.Combobox(frame, textvariable=self.medicine_var, values=med_names, state="readonly")
        combo.pack(pady=5, padx=10, fill=tk.X)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Weekly Adherence", 
                 command=lambda: self.show_adherence("week", med_dict)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Monthly Adherence", 
                 command=lambda: self.show_adherence("month", med_dict)).pack(side=tk.LEFT, padx=5)
        
        self.adherence_text = tk.Text(frame, height=20)
        self.adherence_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.med_dict = med_dict

    def show_adherence(self, period, med_dict):
        selected = self.medicine_var.get()
        if not selected:
            return
        
        med_id = med_dict[selected]
        self.adherence_text.delete(1.0, tk.END)
        
        if period == "week":
            percent = self.db.get_medicine_weekly_adherence(med_id)
            label = "Weekly Adherence"
        else:
            percent = self.db.get_medicine_monthly_adherence(med_id)
            label = "Monthly Adherence"
        
        self.adherence_text.insert(tk.END, f"{label}: {percent}%\n\n")
        
        # Show daily breakdown
        trends = self.db.get_medicine_trends_by_month(med_id)
        self.adherence_text.insert(tk.END, "Monthly Breakdown:\n")
        self.adherence_text.insert(tk.END, "-" * 50 + "\n")
        
        for month, total, taken in trends:
            percentage = int((taken / total) * 100) if total > 0 else 0
            self.adherence_text.insert(tk.END, f"{month}: {taken}/{total} ({percentage}%)\n")

    def create_trends_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Trends")
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Weekly Trends", 
                 command=self.show_weekly_trends).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Monthly Trends", 
                 command=self.show_monthly_trends).pack(side=tk.LEFT, padx=5)
        
        self.trends_text = tk.Text(frame, height=20)
        self.trends_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_weekly_trends(self):
        self.trends_text.delete(1.0, tk.END)
        self.trends_text.insert(tk.END, "Weekly Adherence Trends:\n")
        self.trends_text.insert(tk.END, "=" * 50 + "\n\n")
        
        trends = self.db.get_adherence_trends_by_week()
        for week, total, taken in trends:
            percentage = int((taken / total) * 100) if total > 0 else 0
            self.trends_text.insert(tk.END, f"Week {week}: {taken}/{total} doses ({percentage}%)\n")

    def show_monthly_trends(self):
        self.trends_text.delete(1.0, tk.END)
        self.trends_text.insert(tk.END, "Monthly Adherence Trends:\n")
        self.trends_text.insert(tk.END, "=" * 50 + "\n\n")
        
        trends = self.db.get_adherence_trends_by_month()
        for month, total, taken in trends:
            percentage = int((taken / total) * 100) if total > 0 else 0
            self.trends_text.insert(tk.END, f"{month}: {taken}/{total} doses ({percentage}%)\n")

    def create_missed_doses_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Missed Doses")
        
        tk.Button(frame, text="Generate Missed Doses Report", 
                 command=self.show_missed_report).pack(pady=10)
        
        self.missed_text = tk.Text(frame, height=20)
        self.missed_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_missed_report()

    def show_missed_report(self):
        self.missed_text.delete(1.0, tk.END)
        self.missed_text.insert(tk.END, "Missed Doses Report:\n")
        self.missed_text.insert(tk.END, "=" * 50 + "\n\n")
        
        detail = self.db.get_missed_doses_detail()
        for med_id, med_name, missed, dates in detail:
            self.missed_text.insert(tk.END, f"{med_name}: {missed} missed doses\n")
            if dates:
                self.missed_text.insert(tk.END, f"  Dates: {dates[:100]}...\n")
            self.missed_text.insert(tk.END, "\n")

    def create_streaks_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Streaks")
        
        tk.Button(frame, text="View All Streaks", 
                 command=self.show_streaks).pack(pady=10)
        
        self.streaks_text = tk.Text(frame, height=20)
        self.streaks_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_streaks()

    def show_streaks(self):
        self.streaks_text.delete(1.0, tk.END)
        self.streaks_text.insert(tk.END, "Adherence Streaks:\n")
        self.streaks_text.insert(tk.END, "=" * 70 + "\n\n")
        
        streaks = self.db.get_streaks_all_medicines()
        medicines = {m[0]: m[1] for m in self.db.get_all_medicines()}
        
        for med_id, current, longest in streaks:
            med_name = medicines.get(med_id, "Unknown")
            self.streaks_text.insert(tk.END, f"{med_name}:\n")
            self.streaks_text.insert(tk.END, f"  Current Streak: {current} days\n")
            self.streaks_text.insert(tk.END, f"  Longest Streak: {longest} days\n\n")
