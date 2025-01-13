import sqlite3
from db.config import DatabaseConfig
from db.models.PetDetails import PetDetails


# Класс для управления данными питомцев в БД
class PetRepository:
    def __init__(self):
        self.db_path = DatabaseConfig.DB_PATH

    def create_pet(self, pet: PetDetails):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Создаем запись в PET_DETAILS
        cursor.execute('''
        INSERT INTO PET_DETAILS (
            owner_ID, pet_name, pet_type, pet_sex, pet_birthday, pet_age,
            pet_breed, pet_color, pet_weight, pet_features, pet_visit, visit_ID
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pet.owner_id, pet.pet_name, pet.pet_type, pet.pet_sex,
            pet.pet_birthday, pet.pet_age, pet.pet_breed, pet.pet_color,
            pet.pet_weight, pet.pet_features, pet.pet_visit, pet.visit_id
        ))

        pet.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return pet

    def update_pet(self, pet: PetDetails):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE PET_DETAILS 
        SET owner_ID=?, pet_name=?, pet_type=?, pet_sex=?, pet_birthday=?,
            pet_age=?, pet_breed=?, pet_color=?, pet_weight=?,
            pet_features=?, pet_visit=?, visit_ID=?
        WHERE pet_ID=?
        ''', (
            pet.owner_id, pet.pet_name, pet.pet_type, pet.pet_sex,
            pet.pet_birthday, pet.pet_age, pet.pet_breed, pet.pet_color,
            pet.pet_weight, pet.pet_features, pet.pet_visit, pet.visit_id,
            pet.id
        ))

        conn.commit()
        conn.close()

    def get_pet(self, pet_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM PET_DETAILS
        WHERE pet_ID=?
        ''', (pet_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            pet = PetDetails(
                id=row[0],  # pet_ID
                owner_id=row[1],  # owner_ID
                pet_name=row[2],  # pet_name
                pet_type=row[3],  # pet_type
                pet_sex=row[4],  # pet_sex
                pet_birthday=row[5],  # pet_birthday
                pet_age=row[6],  # pet_age
                pet_breed=row[7],  # pet_breed
                pet_color=row[8],  # pet_color
                pet_weight=row[9],  # pet_weight
                pet_features=row[10],  # pet_features
                pet_visit=row[11],  # pet_visit
                visit_id=row[12],  # visit_ID
            )
            return pet
        return None

    def get_all_pets(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM PET_DETAILS')

        pets = []
        for row in cursor.fetchall():
            pet = PetDetails(
                owner_id=row[1],  # owner_ID
                pet_name=row[2],  # pet_name
                pet_type=row[3],  # pet_type
                pet_sex=row[4],  # pet_sex
                pet_birthday=row[5],  # pet_birthday
                pet_age=row[6],  # pet_age
                pet_breed=row[7],  # pet_breed
                pet_color=row[8],  # pet_color
                pet_weight=row[9],  # pet_weight
                pet_features=row[10],  # pet_features
                pet_visit=row[11],  # pet_visit
                visit_id=row[12],  # visit_ID
                id=row[0]  # pet_ID
            )
            pets.append(pet)

        conn.close()
        return pets

    def delete_pet(self, pet_id):
        """Удаление питомца по ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Получаем информацию о визите питомца
        cursor.execute('SELECT visit_ID FROM PET_DETAILS WHERE pet_ID = ?', (pet_id,))
        visit_id = cursor.fetchone()

        # Если есть связанный визит, удаляем его
        if visit_id and visit_id[0]:
            cursor.execute('DELETE FROM VISIT_DETAILS WHERE visit_ID = ?', (visit_id[0],))

        # Удаляем питомца
        cursor.execute('DELETE FROM PET_DETAILS WHERE pet_ID = ?', (pet_id,))

        conn.commit()
        conn.close()
