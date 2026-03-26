import tkinter as tk
from tkinter import ttk, messagebox
from DATABASE import db

class refill_reminders_window(tk.Toplevel):
    def __init__(self, parent, database: db.database):
        super().__init__(parent)
        self.db = database
        self.title("Medicine Refill Reminders")
        self.geometry("750x650")
        
        self.create_stock_frame()
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_low_stock_tab()
        self.create_all_stock_tab()

    def create_stock_frame(self):
        frame = tk.LabelFrame(self, text="Update Stock", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame, text="Medicine:").pack(anchor=tk.W)
        self.medicine_var = tk.StringVar()
        medicines = self.db.get_all_medicines()
        med_names = [f"{m[1]} ({m[2]})" for m in medicines]
        self.med_dict = {f"{m[1]} ({m[2]})": m[0] for m in medicines}
        
        combo = ttk.Combobox(frame, textvariable=self.medicine_var, values=med_names, state="readonly", width=40)
        combo.pack(anchor=tk.W, pady=5)
        combo.bind("<<ComboboxSelected>>", lambda e: self.load_stock())

        tk.Label(frame, text="Current Stock:").pack(anchor=tk.W)
        self.current_stock_label = tk.Label(frame, text="", font=("Arial", 11), fg="blue")
        self.current_stock_label.pack(anchor=tk.W, pady=5)
        
        tk.Label(frame, text="New Stock Quantity:").pack(anchor=tk.W)
        self.stock_entry = tk.Entry(frame, width=40)
        self.stock_entry.pack(anchor=tk.W, pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(anchor=tk.W, pady=10)
        
        tk.Button(button_frame, text="Update Stock", command=self.update_stock).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Add 10 pills", command=lambda: self.add_stock(10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Add 20 pills", command=lambda: self.add_stock(20)).pack(side=tk.LEFT, padx=5)

    def load_stock(self):
        selected = self.medicine_var.get()
        if not selected:
            return
        
        med_id = self.med_dict[selected]
        stock = self.db.get_stock_quantity(med_id)
        self.current_stock_label.config(text=f"{stock} units")
        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, str(stock))

    def update_stock(self):
        selected = self.medicine_var.get()
        try:
            quantity = int(self.stock_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number")
            return
        
        if not selected:
            messagebox.showwarning("Input Error", "Please select a medicine")
            return
        
        med_id = self.med_dict[selected]
        self.db.update_stock_quantity(med_id, quantity)
        
        messagebox.showinfo("Success", "Stock updated successfully!")
        self.load_stock()
        self.refresh_tabs()

    def add_stock(self, amount):
        selected = self.medicine_var.get()
        if not selected:
            messagebox.showwarning("Input Error", "Please select a medicine")
            return
        
        med_id = self.med_dict[selected]
        current = self.db.get_stock_quantity(med_id)
        new_stock = current + amount
        
        self.db.update_stock_quantity(med_id, new_stock)
        messagebox.showinfo("Success", f"Added {amount} units! New total: {new_stock}")
        
        self.load_stock()
        self.refresh_tabs()

    def create_low_stock_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚠️ Low Stock")
        
        tk.Label(frame, text="Medicines with low stock (≤10 units):", font=("Arial", 12, "bold")).pack(pady=10)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Refresh", command=self.show_low_stock).pack(side=tk.LEFT, padx=5)
        
        self.low_stock_text = tk.Text(frame, height=20)
        self.low_stock_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_low_stock()

    def show_low_stock(self):
        self.low_stock_text.delete(1.0, tk.END)
        low_stock = self.db.get_medicines_low_stock(10)
        
        if not low_stock:
            self.low_stock_text.insert(tk.END, "✅ All medicines have sufficient stock!")
            return
        
        self.low_stock_text.insert(tk.END, "⚠️ MEDICINES NEEDING REFILL:\n")
        self.low_stock_text.insert(tk.END, "=" * 70 + "\n\n")
        
        for med_id, med_name, dosage, stock, times_per_day in low_stock:
            refill_date = self.db.estimate_refill_date(med_id)
            
            self.low_stock_text.insert(tk.END, f"🔴 {med_name} ({dosage})\n")
            self.low_stock_text.insert(tk.END, f"   Current Stock: {stock} units\n")
            self.low_stock_text.insert(tk.END, f"   Usage: {times_per_day} times/day\n")
            self.low_stock_text.insert(tk.END, f"   Estimated Refill Date: {refill_date}\n\n")

    def create_all_stock_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="All Medicines")
        
        tk.Label(frame, text="Stock Status for All Medicines:", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Button(frame, text="Refresh", command=self.show_all_stock).pack(pady=5)
        
        self.all_stock_text = tk.Text(frame, height=20)
        self.all_stock_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_all_stock()

    def show_all_stock(self):
        self.all_stock_text.delete(1.0, tk.END)
        medicines = self.db.get_all_medicines()
        
        if not medicines:
            self.all_stock_text.insert(tk.END, "No medicines found.")
            return
        
        self.all_stock_text.insert(tk.END, "Stock Status - All Medicines:\n")
        self.all_stock_text.insert(tk.END, "=" * 70 + "\n\n")
        
        for med_id, name, dosage, time, times_per_day, days_to_take, stock in medicines:
            refill_date = self.db.estimate_refill_date(med_id)
            
            # Status indicator
            if stock <= 5:
                status = "🔴 CRITICAL"
            elif stock <= 10:
                status = "🟡 LOW"
            else:
                status = "🟢 OK"
            
            self.all_stock_text.insert(tk.END, f"{status} {name} ({dosage})\n")
            self.all_stock_text.insert(tk.END, f"   Stock: {stock} units | Usage: {times_per_day}x/day\n")
            self.all_stock_text.insert(tk.END, f"   Refill estimate: {refill_date}\n\n")

    def refresh_tabs(self):
        self.show_low_stock()
        self.show_all_stock()
