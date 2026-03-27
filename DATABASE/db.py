import sqlite3
from datetime import datetime, timedelta

class database:
    def __init__(self,name="medications.db"):
        self.conn= sqlite3.connect(name)
        self.cursor=self.conn.cursor()
        self.table()

    def table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS medicine (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                             medicine_name TEXT NOT NULL,
                            dosage TEXT NOT NULL,
                            time  DATETIME DEFAULT CURRENT_TIMESTAMP,
                            times_a_day INTEGER NOT NULL,
                            days_to_take INTEGER NOT NULL,
                            stock_quantity INTEGER DEFAULT 0
                            )""")
        
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Adherence (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            med_id INTEGER,
                            date TEXT,
                            taken INTEGER,
                            FOREIGN KEY (med_id) REFERENCES medicine(id)
                            ON UPDATE CASCADE 
                            ON DELETE CASCADE
                            )""")
        
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS SideEffects (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            med_id INTEGER,
                            effect_name TEXT NOT NULL,
                            severity TEXT,
                            date_reported TEXT,
                            FOREIGN KEY (med_id) REFERENCES medicine(id)
                            ON UPDATE CASCADE 
                            ON DELETE CASCADE
                            )""")
        
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS DrugInteractions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            med_id_1 INTEGER,
                            med_id_2 INTEGER,
                            interaction_desc TEXT NOT NULL,
                            severity TEXT,
                            FOREIGN KEY (med_id_1) REFERENCES medicine(id) ON DELETE CASCADE,
                            FOREIGN KEY (med_id_2) REFERENCES medicine(id) ON DELETE CASCADE
                            )""")
        
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS DoctorNotes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            med_id INTEGER,
                            note_text TEXT NOT NULL,
                            date_added TEXT,
                            FOREIGN KEY (med_id) REFERENCES medicine(id)
                            ON UPDATE CASCADE 
                            ON DELETE CASCADE
                            )""")
        
        self.cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS decrement_stock_on_adherence
            AFTER INSERT ON Adherence
            WHEN NEW.taken = 1
            BEGIN
                UPDATE medicine SET stock_quantity = stock_quantity - 1 
                WHERE id = NEW.med_id AND stock_quantity > 0;
            END
        """)
        
        self.conn.commit()
    def get_medicine_adherence_trends(self, med_id):
        self.cursor.execute("""
            SELECT date, taken FROM Adherence 
            WHERE med_id = ? 
            ORDER BY date DESC
        """, (med_id,))
        return self.cursor.fetchall()

    def get_medicine_weekly_adherence(self, med_id):
        date_threshold = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT COUNT(*), SUM(taken) FROM Adherence 
            WHERE med_id = ? AND date >= ?
        """, (med_id, date_threshold))
        total, taken = self.cursor.fetchone()
        if total == 0:
            return 0
        return int((taken / total) * 100)

    def get_medicine_monthly_adherence(self, med_id):
        date_threshold = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT COUNT(*), SUM(taken) FROM Adherence 
            WHERE med_id = ? AND date >= ?
        """, (med_id, date_threshold))
        total, taken = self.cursor.fetchone()
        if total == 0:
            return 0
        return int((taken / total) * 100)
    def get_adherence_trends_by_week(self):
        self.cursor.execute("""
            SELECT strftime('%Y-W%W', date) as week, COUNT(*) as total, SUM(taken) as taken
            FROM Adherence
            GROUP BY strftime('%Y-W%W', date)
            ORDER BY week DESC
            LIMIT 12
        """)
        return self.cursor.fetchall()

    def get_adherence_trends_by_month(self):
        self.cursor.execute("""
            SELECT strftime('%Y-%m', date) as month, COUNT(*) as total, SUM(taken) as taken
            FROM Adherence
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month DESC
            LIMIT 12
        """)
        return self.cursor.fetchall()

    def get_medicine_trends_by_month(self, med_id):
        self.cursor.execute("""
            SELECT strftime('%Y-%m', date) as month, COUNT(*) as total, SUM(taken) as taken
            FROM Adherence
            WHERE med_id = ?
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month DESC
        """, (med_id,))
        return self.cursor.fetchall()
    def get_missed_doses_by_medicine(self):
        self.cursor.execute("""
            SELECT m.id, m.medicine_name, COUNT(a.id) as missed_count
            FROM medicine m
            LEFT JOIN Adherence a ON m.id = a.med_id AND a.taken = 0
            GROUP BY m.id
            ORDER BY missed_count DESC
        """)
        return self.cursor.fetchall()

    def get_missed_doses_by_date_range(self, start_date, end_date):
        self.cursor.execute("""
            SELECT a.id, m.medicine_name, a.date
            FROM Adherence a
            JOIN medicine m ON a.med_id = m.id
            WHERE a.taken = 0 AND a.date BETWEEN ? AND ?
            ORDER BY a.date DESC
        """, (start_date, end_date))
        return self.cursor.fetchall()

    def get_missed_doses_detail(self):
        self.cursor.execute("""
            SELECT m.id, m.medicine_name, COUNT(a.id) as total_missed, 
                   GROUP_CONCAT(a.date) as missed_dates
            FROM medicine m
            LEFT JOIN Adherence a ON m.id = a.med_id AND a.taken = 0
            GROUP BY m.id
            ORDER BY total_missed DESC
        """)
        return self.cursor.fetchall()
    def get_adherence_streak(self, med_id):
        self.cursor.execute("""
            SELECT date FROM Adherence 
            WHERE med_id = ? AND taken = 1
            ORDER BY date DESC
        """, (med_id,))
        dates = self.cursor.fetchall()
        
        if not dates:
            return 0
        
        streak = 0
        today = datetime.now().date()
        
        for idx, (date_str,) in enumerate(dates):
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            expected_date = today - timedelta(days=idx)
            
            if date == expected_date:
                streak += 1
            else:
                break
        
        return streak

    def get_longest_streak(self, med_id):
        self.cursor.execute("""
            SELECT date FROM Adherence 
            WHERE med_id = ? AND taken = 1
            ORDER BY date ASC
        """, (med_id,))
        dates = self.cursor.fetchall()
        
        if not dates:
            return 0
        
        max_streak = 0
        current_streak = 1
        
        for i in range(1, len(dates)):
            date1 = datetime.strptime(dates[i-1][0], "%Y-%m-%d").date()
            date2 = datetime.strptime(dates[i][0], "%Y-%m-%d").date()
            
            if (date2 - date1).days == 1:
                current_streak += 1
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1
        
        return max(max_streak, current_streak)

    def get_streaks_all_medicines(self):
        self.cursor.execute("SELECT id FROM medicine")
        medicines = self.cursor.fetchall()
        
        streaks = []
        for (med_id,) in medicines:
            current = self.get_adherence_streak(med_id)
            longest = self.get_longest_streak(med_id)
            streaks.append((med_id, current, longest))
        
        return streaks
    def update_stock_quantity(self, med_id, quantity):
        self.cursor.execute(
            "UPDATE medicine SET stock_quantity = ? WHERE id = ?",
            (quantity, med_id)
        )
        self.conn.commit()

    def get_stock_quantity(self, med_id):
        self.cursor.execute("SELECT stock_quantity FROM medicine WHERE id = ?", (med_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_medicines_low_stock(self, threshold=10):
        self.cursor.execute("""
            SELECT id, medicine_name, dosage, stock_quantity, times_a_day
            FROM medicine
            WHERE stock_quantity <= ? OR stock_quantity = 0
            ORDER BY stock_quantity ASC
        """, (threshold,))
        return self.cursor.fetchall()

    def estimate_refill_date(self, med_id):
        med = self.get_medicine_by_id(med_id)
        if not med:
            return None
        
        stock = self.get_stock_quantity(med_id)
        times_per_day = med[4]  
        
        if times_per_day == 0:
            return None
        
        days_until_empty = stock // times_per_day if times_per_day > 0 else 0
        refill_date = datetime.now() + timedelta(days=days_until_empty)
        return refill_date.strftime("%Y-%m-%d")
    def add_side_effect(self, med_id, effect_name, severity="mild"):
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            "INSERT INTO SideEffects (med_id, effect_name, severity, date_reported) VALUES (?, ?, ?, ?)",
            (med_id, effect_name, severity, date)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_side_effects_for_medicine(self, med_id):
        self.cursor.execute(
            "SELECT id, effect_name, severity, date_reported FROM SideEffects WHERE med_id = ? ORDER BY date_reported DESC",
            (med_id,)
        )
        return self.cursor.fetchall()

    def get_all_side_effects(self):
        self.cursor.execute("""
            SELECT m.id, m.medicine_name, COUNT(s.id) as effect_count, GROUP_CONCAT(s.effect_name) as effects
            FROM medicine m
            LEFT JOIN SideEffects s ON m.id = s.med_id
            GROUP BY m.id
            ORDER BY effect_count DESC
        """)
        return self.cursor.fetchall()

    def delete_side_effect(self, effect_id):
        self.cursor.execute("DELETE FROM SideEffects WHERE id = ?", (effect_id,))
        self.conn.commit()

    def get_common_side_effects(self):
        self.cursor.execute("""
            SELECT effect_name, COUNT(*) as count, severity
            FROM SideEffects
            GROUP BY effect_name
            ORDER BY count DESC
            LIMIT 10
        """)
        return self.cursor.fetchall()
    def add_interaction(self, med_id_1, med_id_2, interaction_desc, severity="moderate"):
        self.cursor.execute(
            "INSERT INTO DrugInteractions (med_id_1, med_id_2, interaction_desc, severity) VALUES (?, ?, ?, ?)",
            (med_id_1, med_id_2, interaction_desc, severity)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_interactions_for_medicine(self, med_id):
        self.cursor.execute("""
            SELECT di.id, m1.medicine_name, m2.medicine_name, di.interaction_desc, di.severity
            FROM DrugInteractions di
            JOIN medicine m1 ON di.med_id_1 = m1.id
            JOIN medicine m2 ON di.med_id_2 = m2.id
            WHERE di.med_id_1 = ? OR di.med_id_2 = ?
        """, (med_id, med_id))
        return self.cursor.fetchall()

    def check_interactions(self, med_id):
        medicines = self.get_all_medicines()
        med_ids = [m[0] for m in medicines]
        
        interactions = []
        for other_id in med_ids:
            if other_id != med_id:
                result = self.cursor.execute(
                    "SELECT * FROM DrugInteractions WHERE (med_id_1 = ? AND med_id_2 = ?) OR (med_id_1 = ? AND med_id_2 = ?)",
                    (med_id, other_id, other_id, med_id)
                ).fetchone()
                if result:
                    interactions.append(result)
        
        return interactions

    def get_all_interactions(self):
        self.cursor.execute("""
            SELECT di.id, m1.medicine_name, m2.medicine_name, di.interaction_desc, di.severity
            FROM DrugInteractions di
            JOIN medicine m1 ON di.med_id_1 = m1.id
            JOIN medicine m2 ON di.med_id_2 = m2.id
            ORDER BY di.severity DESC
        """)
        return self.cursor.fetchall()

    def delete_interaction(self, interaction_id):
        self.cursor.execute("DELETE FROM DrugInteractions WHERE id = ?", (interaction_id,))
        self.conn.commit()

    def get_high_severity_interactions(self):
        self.cursor.execute("""
            SELECT di.id, m1.medicine_name, m2.medicine_name, di.interaction_desc
            FROM DrugInteractions di
            JOIN medicine m1 ON di.med_id_1 = m1.id
            JOIN medicine m2 ON di.med_id_2 = m2.id
            WHERE di.severity = 'high'
        """)
        return self.cursor.fetchall()
    def add_doctor_note(self, med_id, note_text):
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            "INSERT INTO DoctorNotes (med_id, note_text, date_added) VALUES (?, ?, ?)",
            (med_id, note_text, date)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_doctor_notes_for_medicine(self, med_id):
        self.cursor.execute(
            "SELECT id, note_text, date_added FROM DoctorNotes WHERE med_id = ? ORDER BY date_added DESC",
            (med_id,)
        )
        return self.cursor.fetchall()

    def get_all_doctor_notes(self):
        self.cursor.execute("""
            SELECT m.id, m.medicine_name, dn.note_text, dn.date_added
            FROM DoctorNotes dn
            JOIN medicine m ON dn.med_id = m.id
            ORDER BY dn.date_added DESC
        """)
        return self.cursor.fetchall()

    def update_doctor_note(self, note_id, note_text):
        self.cursor.execute(
            "UPDATE DoctorNotes SET note_text = ? WHERE id = ?",
            (note_text, note_id)
        )
        self.conn.commit()

    def delete_doctor_note(self, note_id):
        self.cursor.execute("DELETE FROM DoctorNotes WHERE id = ?", (note_id,))
        self.conn.commit()
    def add_medicine(self, medicine_name, dosage, times_a_day, days_to_take):
        self.cursor.execute(
            "INSERT INTO medicine (medicine_name, dosage, times_a_day, days_to_take) VALUES (?, ?, ?, ?)",
            (medicine_name, dosage, times_a_day, days_to_take)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_medicines(self):
        self.cursor.execute("SELECT * FROM medicine")
        return self.cursor.fetchall()

    def get_medicine_by_id(self, med_id):
        self.cursor.execute("SELECT * FROM medicine WHERE id = ?", (med_id,))
        return self.cursor.fetchone()

    def get_medicine_by_name(self, medicine_name):
        self.cursor.execute("SELECT * FROM medicine WHERE medicine_name LIKE ?", (f"%{medicine_name}%",))
        return self.cursor.fetchall()

    def update_medicine(self, med_id, medicine_name, dosage, times_a_day, days_to_take):
        self.cursor.execute(
            "UPDATE medicine SET medicine_name = ?, dosage = ?, times_a_day = ?, days_to_take = ? WHERE id = ?",
            (medicine_name, dosage, times_a_day, days_to_take, med_id)
        )
        self.conn.commit()

    def delete_medicine(self, med_id):
        self.cursor.execute("DELETE FROM medicine WHERE id = ?", (med_id,))
        self.conn.commit()
