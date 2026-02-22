from datetime import datetime
from DATABASE import db
class AdherenceAnalytics:
    def __init__(self):
        self.db = db

    def mark_taken(self, med_id, taken=True):
        date = datetime.now().strftime("%Y-%m-%d")
        self.db.cursor.execute(
            "INSERT INTO Adherence(med_id, date, taken) VALUES (?, ?, ?)",
            (med_id, date, int(taken))
        )
        self.db.conn.commit()

    def overall_adherence(self):
        self.db.cursor.execute("SELECT COUNT(*), SUM(taken) FROM Adherence")
        total, taken = self.db.cursor.fetchone()
        if total == 0:
            return 0
        return int((taken / total) * 100)