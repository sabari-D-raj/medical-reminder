import tkinter as tk
from tkinter import ttk, messagebox
from DATABASE import db

class interactions_window(tk.Toplevel):
    def __init__(self, parent, database: db.database):
        super().__init__(parent)
        self.db = database
        self.title("Drug Interactions Manager")
        self.geometry("800x650")
        
        self.create_add_frame()
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_all_interactions_tab()
        self.create_high_severity_tab()
        self.create_check_tab()

    def create_add_frame(self):
        frame = tk.LabelFrame(self, text="Add Drug Interaction", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame, text="Medicine 1:").pack(anchor=tk.W)
        self.med1_var = tk.StringVar()
        medicines = self.db.get_all_medicines()
        med_names = [f"{m[1]} ({m[2]})" for m in medicines]
        self.med_dict = {f"{m[1]} ({m[2]})": m[0] for m in medicines}
        
        combo1 = ttk.Combobox(frame, textvariable=self.med1_var, values=med_names, state="readonly", width=35)
        combo1.pack(anchor=tk.W, pady=5)
        

        tk.Label(frame, text="Medicine 2:").pack(anchor=tk.W)
        self.med2_var = tk.StringVar()
        combo2 = ttk.Combobox(frame, textvariable=self.med2_var, values=med_names, state="readonly", width=35)
        combo2.pack(anchor=tk.W, pady=5)
        

        tk.Label(frame, text="Interaction Description:").pack(anchor=tk.W)
        self.desc_entry = tk.Entry(frame, width=40)
        self.desc_entry.pack(anchor=tk.W, pady=5)
        

        tk.Label(frame, text="Severity:").pack(anchor=tk.W)
        self.severity_var = tk.StringVar(value="moderate")
        severity_combo = ttk.Combobox(frame, textvariable=self.severity_var,
                                      values=["low", "moderate", "high"], state="readonly", width=37)
        severity_combo.pack(anchor=tk.W, pady=5)
        
        tk.Button(frame, text="Add Interaction", command=self.add_interaction).pack(pady=10)

    def add_interaction(self):
        med1 = self.med1_var.get()
        med2 = self.med2_var.get()
        desc = self.desc_entry.get()
        severity = self.severity_var.get()
        
        if not med1 or not med2 or not desc:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return
        
        if med1 == med2:
            messagebox.showwarning("Error", "Please select different medicines")
            return
        
        med_id_1 = self.med_dict[med1]
        med_id_2 = self.med_dict[med2]
        
        self.db.add_interaction(med_id_1, med_id_2, desc, severity)
        messagebox.showinfo("Success", "Interaction added successfully!")
        
        self.desc_entry.delete(0, tk.END)
        self.refresh_tabs()

    def create_all_interactions_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="All Interactions")
        
        tk.Button(frame, text="Refresh", command=self.show_all_interactions).pack(pady=10)
        
        self.all_text = tk.Text(frame, height=20)
        self.all_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_all_interactions()

    def show_all_interactions(self):
        self.all_text.delete(1.0, tk.END)
        interactions = self.db.get_all_interactions()
        
        if not interactions:
            self.all_text.insert(tk.END, "No drug interactions recorded.")
            return
        
        self.all_text.insert(tk.END, "All Drug Interactions:\n")
        self.all_text.insert(tk.END, "=" * 80 + "\n\n")
        
        for inter_id, med1, med2, desc, severity in interactions:
            color_code = "🔴" if severity == "high" else "🟡" if severity == "moderate" else "🟢"
            self.all_text.insert(tk.END, f"{color_code} {med1} ↔ {med2} ({severity})\n")
            self.all_text.insert(tk.END, f"   {desc}\n\n")

    def create_high_severity_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="High Severity ⚠️")
        
        tk.Button(frame, text="Refresh", command=self.show_high_severity).pack(pady=10)
        
        self.high_text = tk.Text(frame, height=20)
        self.high_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_high_severity()

    def show_high_severity(self):
        self.high_text.delete(1.0, tk.END)
        interactions = self.db.get_high_severity_interactions()
        
        if not interactions:
            self.high_text.insert(tk.END, "No high severity interactions recorded.")
            return
        
        self.high_text.insert(tk.END, "HIGH SEVERITY Drug Interactions:\n")
        self.high_text.insert(tk.END, "⚠️ " * 20 + "\n\n")
        
        for inter_id, med1, med2, desc in interactions:
            self.high_text.insert(tk.END, f"🔴 {med1} ↔ {med2}\n")
            self.high_text.insert(tk.END, f"   {desc}\n\n")

    def create_check_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Check Medicine")
        
        tk.Label(frame, text="Select Medicine to Check:").pack(pady=10)
        
        self.check_var = tk.StringVar()
        medicines = self.db.get_all_medicines()
        med_names = [f"{m[1]} ({m[2]})" for m in medicines]
        self.med_dict2 = {f"{m[1]} ({m[2]})": m[0] for m in medicines}
        
        combo = ttk.Combobox(frame, textvariable=self.check_var, values=med_names, state="readonly")
        combo.pack(pady=5, padx=10, fill=tk.X)
        combo.bind("<<ComboboxSelected>>", lambda e: self.check_medicine())
        
        self.check_text = tk.Text(frame, height=20)
        self.check_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def check_medicine(self):
        selected = self.check_var.get()
        if not selected:
            return
        
        med_id = self.med_dict2[selected]
        
        self.check_text.delete(1.0, tk.END)
        self.check_text.insert(tk.END, f"Checking interactions for: {selected}\n")
        self.check_text.insert(tk.END, "=" * 70 + "\n\n")
        
        interactions = self.db.get_interactions_for_medicine(med_id)
        
        if not interactions:
            self.check_text.insert(tk.END, "No interactions found for this medicine.")
            return
        
        for inter_id, med1, med2, desc, severity in interactions:
            color_code = "🔴" if severity == "high" else "🟡" if severity == "moderate" else "🟢"
            self.check_text.insert(tk.END, f"{color_code} {med1} ↔ {med2} ({severity})\n")
            self.check_text.insert(tk.END, f"   {desc}\n\n")

    def refresh_tabs(self):
        self.show_all_interactions()
        self.show_high_severity()
