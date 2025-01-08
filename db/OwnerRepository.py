import sqlite3
from db.config import DatabaseConfig
from db.models.OwnerDetails import OwnerDetails

# Класс для управления данными владельцев в БД
class OwnerRepository:
    def __init__(self):
        self.db_path = DatabaseConfig.DB_PATH

    def create_owner(self, owner: OwnerDetails):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO OWNER_DETAILS (owner_lastname, owner_name, owner_patronymic, owner_phone, owner_email)
        VALUES (?, ?, ?, ?, ?)
        ''', (owner.owner_lastname, owner.owner_name, owner.owner_patronymic,
              owner.owner_phone, owner.owner_email))

        owner.id = cursor.lastrowid

        conn.commit()
        conn.close()

        return owner

    def update_owner(self, owner: OwnerDetails):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE OWNER_DETAILS 
        SET owner_lastname=?, owner_name=?, owner_patronymic=?, owner_phone=?, owner_email=?
        WHERE owner_ID=?
        ''', (owner.owner_lastname, owner.owner_name, owner.owner_patronymic,
              owner.owner_phone, owner.owner_email, owner.id))

        conn.commit()
        conn.close()

    def get_owner(self, owner_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT owner_lastname, owner_name, owner_patronymic, owner_phone, owner_email
        FROM OWNER_DETAILS
        WHERE owner_ID=?
        ''', (owner_id,))

        owner_row = cursor.fetchone()
        conn.close()

        if owner_row:
            owner = OwnerDetails(owner_row[0], owner_row[1], owner_row[2], owner_row[3], owner_row[4], owner_id)
            return owner
        return None

    def get_all_owners(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT owner_ID, owner_lastname, owner_name, owner_patronymic, owner_phone, owner_email
        FROM OWNER_DETAILS
        ORDER BY owner_lastname, owner_name, owner_patronymic
        ''')

        owners = []
        for row in cursor.fetchall():
            owner = OwnerDetails(
                owner_lastname=row[1],
                owner_name=row[2],
                owner_patronymic=row[3],
                owner_phone=row[4],
                owner_email=row[5]
            )
            owner.id = row[0]
            owners.append(owner)

        conn.close()
        return owners