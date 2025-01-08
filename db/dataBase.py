import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem
from db.config import DatabaseConfig

conn = sqlite3.connect(DatabaseConfig.DB_PATH)
cursor = conn.cursor()

# Создание таблицы PET_LIST
cursor.execute('''
CREATE TABLE IF NOT EXISTS PET_LIST (
    pet_ID INTEGER PRIMARY KEY,
    owner_ID INTEGER,
    pet_name TEXT NOT NULL,
    owner_FIO TEXT NOT NULL,
    FOREIGN KEY (owner_ID) REFERENCES OWNER_DETAILS(owner_ID)
)
''')

# Создание таблицы OWNER_DETAILS
cursor.execute('''
CREATE TABLE IF NOT EXISTS OWNER_DETAILS (
    owner_ID INTEGER PRIMARY KEY,
    owner_lastname TEXT NOT NULL,
    owner_name TEXT NOT NULL,
    owner_patronymic TEXT,
    owner_phone TEXT,
    owner_email TEXT
)
''')

# Создание таблицы PET_DETAILS
cursor.execute('''
CREATE TABLE IF NOT EXISTS PET_DETAILS (
    pet_ID INTEGER PRIMARY KEY,
    owner_ID INTEGER,
    pet_name TEXT NOT NULL,
    pet_type TEXT,
    pet_sex TEXT,
    pet_birthday date,
    pet_age TEXT,
    pet_breed TEXT,
    pet_color TEXT,
    pet_weight INTEGER,
    pet_features TEXT,
    pet_visit date,
    visit_ID INTEGER,
    FOREIGN KEY (visit_ID) REFERENCES VISIT_DETAILS(visit_ID),
    FOREIGN KEY (owner_ID) REFERENCES OWNER_DETAILS(owner_ID)
)
''')

# Создание таблицы VISIT_DETAILS
cursor.execute('''
CREATE TABLE IF NOT EXISTS VISIT_DETAILS (
    visit_ID INTEGER PRIMARY KEY,
    pet_visit DATE,
    pet_complaints TEXT,
    pet_diagnosis TEXT,
    pet_analyses TEXT,
    pet_treatment TEXT
)
''')

print("База данных и таблицы успешно созданы!")
