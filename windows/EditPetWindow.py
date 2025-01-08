from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui import Ui_EditPet
from db.PetRepository import PetRepository
from db.OwnerRepository import OwnerRepository
from db.models.PetDetails import PetDetails
from db.VisitRepository import VisitRepository
from db.models.VisitDetails import VisitDetails


# Окно изменения животного
class EditPetWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = Ui_EditPet()
        self.ui.setupUi(self)

        # Создание объектов для общения с БД
        self.pet_repository = PetRepository()
        self.owner_repository = OwnerRepository()
        self.visit_repository = VisitRepository()

        # Определение функционала кнопок
        self.ui.pushButton.clicked.connect(self.back_to_previous)
        self.ui.pushButton_2.clicked.connect(self.close_application)
        self.ui.pushButton_3.clicked.connect(self.save_changes)
        self.ui.pushButton_4.clicked.connect(self.back_to_previous)
        # Отключение изменение владельца
        self.ui.lineEdit_2.setEnabled(False)

        # Создание переменных для работы окна
        self.current_pet_id = None
        self.current_pet = None
        self.current_owner_id = None
        self.previous_window = None

    # Загрузка данных животного
    def load_pet_data(self, pet_id, previous_window=None):
        self.current_pet_id = pet_id
        # Сохранение предыдущего окна
        self.previous_window = previous_window or self.parent.card_list_menu

        # Поиск животного в бд
        self.current_pet = self.pet_repository.get_pet(pet_id)
        self.current_owner_id = self.current_pet.owner_id

        # Заполнение полей формы данными из БД
        self.ui.lineEdit.setText(self.current_pet.pet_name)
        owner = self.owner_repository.get_owner(self.current_pet.owner_id)
        self.ui.lineEdit_2.setText(f"{owner.owner_lastname} {owner.owner_name} {owner.owner_patronymic}")
        self.ui.lineEdit_3.setText(self.current_pet.pet_type)
        self.ui.lineEdit_4.setText(self.current_pet.pet_sex)
        self.ui.lineEdit_5.setText(str(self.current_pet.pet_birthday))
        self.ui.lineEdit_6.setText(str(self.current_pet.pet_age))
        self.ui.lineEdit_7.setText(self.current_pet.pet_breed)
        self.ui.lineEdit_8.setText(self.current_pet.pet_color)
        self.ui.lineEdit_9.setText(str(self.current_pet.pet_weight))
        self.ui.lineEdit_10.setText(self.current_pet.pet_features)

        # Поиск визита животного в БД
        visit = self.visit_repository.get_visit(self.current_pet.visit_id)

        # Заполнение полей формы данными из БД
        if visit:
            self.ui.lineEdit_20.setText(str(visit.pet_visit))
            self.ui.textEdit_3.setText(visit.pet_complaints)
            self.ui.lineEdit_22.setText(visit.pet_diagnosis)
            self.ui.textEdit_2.setText(visit.pet_analyses)
            self.ui.textEdit.setText(visit.pet_treatment)
        else:
            self.ui.lineEdit_20.setText("-")
            self.ui.textEdit_3.setText("-")
            self.ui.lineEdit_22.setText("-")
            self.ui.textEdit_2.setText("-")
            self.ui.textEdit.setText("-")

    # Сохранение изменений
    def save_changes(self):
        # Получения аднных с формы
        pet_name = self.ui.lineEdit.text()
        pet_type = self.ui.lineEdit_3.text()
        pet_sex = self.ui.lineEdit_4.text()
        pet_birthday = self.ui.lineEdit_5.text()
        pet_age = self.ui.lineEdit_6.text()
        pet_breed = self.ui.lineEdit_7.text()
        pet_color = self.ui.lineEdit_8.text()
        pet_weight = self.ui.lineEdit_9.text()
        pet_features = self.ui.lineEdit_10.text()

        # Проверка обязательных полей
        if not pet_name or not pet_type:
            QMessageBox.warning(self, "Ошибка", "Кличка и вид животного обязательны для заполнения!")
            return

        # Изменение данных животного
        self.current_pet.pet_name = pet_name
        self.current_pet.pet_type = pet_type
        self.current_pet.pet_sex = pet_sex
        self.current_pet.pet_birthday = pet_birthday
        self.current_pet.pet_age = pet_age
        self.current_pet.pet_breed = pet_breed
        self.current_pet.pet_color = pet_color
        self.current_pet.pet_weight = pet_weight
        self.current_pet.pet_features = pet_features

        # Поиск визита животного
        visit = self.visit_repository.get_visit(self.current_pet.visit_id)
        # Изменение данных визита
        if visit:
            # Если найдено в БД, то изменяем
            visit.pet_visit = self.ui.lineEdit_20.text()
            visit.pet_complaints = self.ui.textEdit_3.toPlainText()
            visit.pet_diagnosis = self.ui.lineEdit_22.text()
            visit.pet_analyses = self.ui.textEdit_2.toPlainText()
            visit.pet_treatment = self.ui.textEdit.toPlainText()
            self.visit_repository.update_visit(visit)
        else:
            # Если не найдено в БД, то создаем
            visit = VisitDetails(
                pet_visit=self.ui.lineEdit_20.text(),
                pet_complaints=self.ui.textEdit_3.toPlainText(),
                pet_diagnosis=self.ui.lineEdit_22.text(),
                pet_analyses=self.ui.textEdit_2.toPlainText(),
                pet_treatment=self.ui.textEdit.toPlainText()
            )
            visit = self.visit_repository.create_visit(visit)
            self.current_pet.visit_id = visit.id
            self.current_pet.pet_visit = visit.pet_visit

        # Сохранение животного
        self.pet_repository.update_pet(self.current_pet)
        self.back_to_previous()

    # Возврат в прошлое меню
    def back_to_previous(self):
        if self.previous_window:
            # Если возвращаемся в окно карточки питомца, обновляем данные
            if hasattr(self.previous_window, 'load_pet_data') and self.current_pet_id:
                self.previous_window.load_pet_data(self.current_pet_id)
            self.parent.stacked_widget.setCurrentWidget(self.previous_window)
        else:
            self.parent.stacked_widget.setCurrentWidget(self.parent.card_list_menu)
        self.current_pet_id = None
        self.current_owner_id = None
        self.previous_window = None

    # Закрытие приложения
    def close_application(self):
        """Закрытие приложения"""
        self.parent.close()
