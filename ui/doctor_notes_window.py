import tkinter as tk
from tkinter import ttk, messagebox
from DATABASE import db

class doctor_notes_window(tk.Toplevel):
    def __init__(self, parent, database: db.database):
        super().__init__(parent)
        self.db = database
        self.title("Doctor Notes Manager")
        self.geometry("750x650")
        
        self.create_add_frame()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_by_medicine_tab()
        self.create_all_notes_tab()

    def create_add_frame(self):
        frame = tk.LabelFrame(self, text="Add Doctor's Note", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame, text="Medicine:").pack(anchor=tk.W)
        self.medicine_var = tk.StringVar()
        medicines = self.db.get_all_medicines()
        med_names = [f"{m[1]} ({m[2]})" for m in medicines]
        self.med_dict = {f"{m[1]} ({m[2]})": m[0] for m in medicines}
        
        combo = ttk.Combobox(frame, textvariable=self.medicine_var, values=med_names, state="readonly", width=40)
        combo.pack(anchor=tk.W, pady=5)
        
        tk.Label(frame, text="Doctor's Note:").pack(anchor=tk.W)
        self.note_entry = tk.Text(frame, height=4, width=50)
        self.note_entry.pack(anchor=tk.W, pady=5)
        
        tk.Button(frame, text="Add Note", command=self.add_note).pack(pady=10)

    def add_note(self):
        selected = self.medicine_var.get()
        note = self.note_entry.get(1.0, tk.END).strip()
        
        if not selected or not note:
            messagebox.showwarning("Input Error", "Please select medicine and enter note")
            return
        
        med_id = self.med_dict[selected]
        self.db.add_doctor_note(med_id, note)
        
        messagebox.showinfo("Success", "Note added successfully!")
        self.note_entry.delete(1.0, tk.END)
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
        combo.bind("<<ComboboxSelected>>", lambda e: self.show_medicine_notes())
        
        self.notes_frame = tk.Frame(frame)
        self.notes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_medicine_notes(self):
        selected = self.med_var.get()
        if not selected:
            return
        
        med_id = self.med_dict2[selected]
        
        for widget in self.notes_frame.winfo_children():
            widget.destroy()
        
        notes = self.db.get_doctor_notes_for_medicine(med_id)
        
        if not notes:
            tk.Label(self.notes_frame, text="No doctor notes for this medicine").pack(pady=10)
            return
        
        canvas = tk.Canvas(self.notes_frame)
        scrollbar = ttk.Scrollbar(self.notes_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.note_entries = {}
        
        for note_id, note_text, date in notes:
            note_frame = tk.Frame(scrollable_frame, relief=tk.RIDGE, borderwidth=2, bg="lightyellow")
            note_frame.pack(fill=tk.BOTH, pady=5)
            
            header_frame = tk.Frame(note_frame, bg="lightyellow")
            header_frame.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(header_frame, text=f"Added: {date}", font=("Arial", 9), 
                    fg="gray", bg="lightyellow").pack(anchor=tk.W)
            
            text_widget = tk.Text(note_frame, height=3, width=70, wrap=tk.WORD, bg="white")
            text_widget.pack(fill=tk.BOTH, padx=5, pady=5, expand=False)
            text_widget.insert(1.0, note_text)
            
            self.note_entries[note_id] = text_widget
            
            button_frame = tk.Frame(note_frame, bg="lightyellow")
            button_frame.pack(anchor=tk.E, padx=5, pady=5)
            
            tk.Button(button_frame, text="Update", 
                     command=lambda nid=note_id: self.update_note(nid)).pack(side=tk.LEFT, padx=2)
            tk.Button(button_frame, text="Delete", 
                     command=lambda nid=note_id: self.delete_note(nid)).pack(side=tk.LEFT, padx=2)
        
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_note(self, note_id):
        if note_id in self.note_entries:
            new_text = self.note_entries[note_id].get(1.0, tk.END).strip()
            self.db.update_doctor_note(note_id, new_text)
            messagebox.showinfo("Success", "Note updated!")
            self.show_medicine_notes()

    def delete_note(self, note_id):
        if messagebox.askyesno("Confirm", "Delete this note?"):
            self.db.delete_doctor_note(note_id)
            self.show_medicine_notes()
            self.refresh_tabs()

    def create_all_notes_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="All Notes")
        
        tk.Button(frame, text="Refresh", command=self.show_all_notes).pack(pady=10)
        
        self.all_notes_text = tk.Text(frame, height=20)
        self.all_notes_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_all_notes()

    def show_all_notes(self):
        self.all_notes_text.delete(1.0, tk.END)
        notes = self.db.get_all_doctor_notes()
        
        if not notes:
            self.all_notes_text.insert(tk.END, "No doctor notes recorded.")
            return
        
        self.all_notes_text.insert(tk.END, "All Doctor's Notes:\n")
        self.all_notes_text.insert(tk.END, "=" * 70 + "\n\n")
        
        for med_id, med_name, note, date in notes:
            self.all_notes_text.insert(tk.END, f"📋 {med_name}\n")
            self.all_notes_text.insert(tk.END, f"   Date: {date}\n")
            self.all_notes_text.insert(tk.END, f"   Note: {note}\n\n")

    def refresh_tabs(self):
        self.show_all_notes()
