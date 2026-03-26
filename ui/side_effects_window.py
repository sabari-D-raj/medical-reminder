import tkinter as tk
from tkinter import ttk, messagebox
from DATABASE import db

class side_effects_window(tk.Toplevel):
    def __init__(self, parent, database: db.database):
        super().__init__(parent)
        self.db = database
        self.title("Side Effects Tracker")
        self.geometry("700x600")
        
        self.create_add_frame()
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_by_medicine_tab()
        self.create_common_tab()

    def create_add_frame(self):
        frame = tk.LabelFrame(self, text="Add Side Effect", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame, text="Medicine:").pack(anchor=tk.W)
        self.medicine_var = tk.StringVar()
        medicines = self.db.get_all_medicines()
        med_names = [f"{m[1]} ({m[2]})" for m in medicines]
        self.med_dict = {f"{m[1]} ({m[2]})": m[0] for m in medicines}
        
        combo = ttk.Combobox(frame, textvariable=self.medicine_var, values=med_names, state="readonly", width=40)
        combo.pack(anchor=tk.W, pady=5)
        
        tk.Label(frame, text="Effect Name:").pack(anchor=tk.W)
        self.effect_entry = tk.Entry(frame, width=40)
        self.effect_entry.pack(anchor=tk.W, pady=5)
        

        tk.Label(frame, text="Severity:").pack(anchor=tk.W)
        self.severity_var = tk.StringVar(value="mild")
        severity_combo = ttk.Combobox(frame, textvariable=self.severity_var, 
                                      values=["mild", "moderate", "severe"], state="readonly", width=37)
        severity_combo.pack(anchor=tk.W, pady=5)
        
        tk.Button(frame, text="Add Side Effect", command=self.add_side_effect).pack(pady=10)

    def add_side_effect(self):
        selected = self.medicine_var.get()
        effect = self.effect_entry.get()
        severity = self.severity_var.get()
        
        if not selected or not effect:
            messagebox.showwarning("Input Error", "Please select medicine and enter effect name")
            return
        
        med_id = self.med_dict[selected]
        self.db.add_side_effect(med_id, effect, severity)
        
        messagebox.showinfo("Success", "Side effect added successfully!")
        self.effect_entry.delete(0, tk.END)
        self.refresh_tabs()

    def create_by_medicine_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="By Medicine")
        
        tk.Label(frame, text="Select Medicine:").pack(pady=10)
        
        self.med_var = tk.StringVar()
        medicines = self.db.get_all_medicines()
        med_names = [f"{m[1]} ({m[2]})" for m in medicines]
        self.med_dict2 = {f"{m[1]} ({m[2]})": m[0] for m in medicines}
        
        combo = ttk.Combobox(frame, textvariable=self.med_var, values=med_names, state="readonly")
        combo.pack(pady=5, padx=10, fill=tk.X)
        combo.bind("<<ComboboxSelected>>", lambda e: self.show_medicine_effects())
        
        self.effects_frame = tk.Frame(frame)
        self.effects_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_medicine_effects(self):
        selected = self.med_var.get()
        if not selected:
            return
        
        med_id = self.med_dict2[selected]
        
        for widget in self.effects_frame.winfo_children():
            widget.destroy()
        
        effects = self.db.get_side_effects_for_medicine(med_id)
        
        if not effects:
            tk.Label(self.effects_frame, text="No side effects recorded").pack(pady=10)
            return
        canvas = tk.Canvas(self.effects_frame)
        scrollbar = ttk.Scrollbar(self.effects_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for effect_id, effect_name, severity, date in effects:
            effect_frame = tk.Frame(scrollable_frame, relief=tk.RIDGE, borderwidth=1)
            effect_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(effect_frame, text=f"{effect_name} ({severity})", font=("Arial", 11)).pack(anchor=tk.W, padx=5, pady=2)
            tk.Label(effect_frame, text=f"Reported: {date}", font=("Arial", 9), fg="gray").pack(anchor=tk.W, padx=5, pady=2)
            
            delete_btn = tk.Button(effect_frame, text="Delete", font=("Arial", 8),
                                   command=lambda eid=effect_id: self.delete_effect(eid))
            delete_btn.pack(anchor=tk.E, padx=5, pady=2)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

    def delete_effect(self, effect_id):
        if messagebox.askyesno("Confirm", "Delete this side effect?"):
            self.db.delete_side_effect(effect_id)
            self.show_medicine_effects()
            self.refresh_tabs()

    def create_common_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Most Common")
        
        tk.Label(frame, text="Most Common Side Effects:").pack(pady=10)
        
        self.common_text = tk.Text(frame, height=20)
        self.common_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_common_effects()

    def show_common_effects(self):
        self.common_text.delete(1.0, tk.END)
        common = self.db.get_common_side_effects()
        
        self.common_text.insert(tk.END, "Most Common Side Effects:\n")
        self.common_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for effect, count, severity in common:
            self.common_text.insert(tk.END, f"{effect}\n")
            self.common_text.insert(tk.END, f"  Occurrences: {count}, Severity: {severity}\n\n")

    def refresh_tabs(self):
        self.show_common_effects()
