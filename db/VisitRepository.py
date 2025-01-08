import sqlite3
from db.config import DatabaseConfig
from db.models.VisitDetails import VisitDetails

# Класс для управления данными визитов в БД
class VisitRepository:
    def __init__(self):
        self.db_path = DatabaseConfig.DB_PATH

    def create_visit(self, visit: VisitDetails):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO VISIT_DETAILS (pet_visit, pet_complaints, pet_diagnosis, pet_analyses, pet_treatment)
        VALUES (?, ?, ?, ?, ?)
        ''', (visit.pet_visit, visit.pet_complaints,
              visit.pet_diagnosis, visit.pet_analyses,
              visit.pet_treatment))

        visit.id = cursor.lastrowid

        conn.commit()
        conn.close()

        return visit

    def update_visit(self, visit: VisitDetails):
        """Обновление данных визита"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE VISIT_DETAILS 
        SET pet_visit=?, pet_complaints=?, pet_diagnosis=?, pet_analyses=?, pet_treatment=?
        WHERE visit_ID=?
        ''', (visit.pet_visit, visit.pet_complaints,
              visit.pet_diagnosis, visit.pet_analyses,
              visit.pet_treatment, visit.id))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def get_visit(self, visit_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT *
        FROM VISIT_DETAILS
        WHERE visit_ID=?
        ''', (visit_id,))

        visit_row = cursor.fetchone()
        conn.close()

        if visit_row:
            visit = VisitDetails(
                visit_row[1],
                visit_row[2],
                visit_row[3],
                visit_row[4],
                visit_row[5],
                visit_row[0]
            )
            return visit
        return None