from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from ui import Ui_petCard
from db.PetRepository import PetRepository
from db.OwnerRepository import OwnerRepository
from db.VisitRepository import VisitRepository


# Окно карточки животного
class PetCardWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = Ui_petCard()
        self.ui.setupUi(self)

        # Создание объектов для общения с БД
        self.pet_repository = PetRepository()
        self.owner_repository = OwnerRepository()
        self.visit_repository = VisitRepository()

        # Определение функционала кнопок
        self.ui.pushButton_14.clicked.connect(self.back_to_list)
        self.ui.pushButton_15.clicked.connect(self.close_application)
        self.ui.pushButton_17.clicked.connect(self.edit_owner)
        self.ui.pushButton_16.clicked.connect(self.edit_pet)

        # Определение объектов для работы окна
        self.current_pet_id = None
        self.current_pet = None
        self.current_owner_id = None

    # Метод который срабаотывает при каждом отбражении окна, обновляет данные животного
    def showEvent(self, event):
        self.load_pet_data(self.current_pet_id)
        super().showEvent(event)

    # Загрузка данных животного
    def load_pet_data(self, pet_id):
        self.current_pet_id = pet_id
        # Поиск животного в БД
        self.current_pet = self.pet_repository.get_pet(pet_id)

        # Заполняем поля формы из БД
        self.ui.label_97.setText(self.current_pet.pet_name)
        self.ui.label_99.setText(self.current_pet.pet_type)
        self.ui.label_96.setText(self.current_pet.pet_type + " " + self.current_pet.pet_name)
        self.ui.label_100.setText(self.current_pet.pet_sex)
        self.ui.label_101.setText(str(self.current_pet.pet_birthday))
        self.ui.label_102.setText(str(self.current_pet.pet_age))
        self.ui.label_103.setText(self.current_pet.pet_breed)
        self.ui.label_104.setText(self.current_pet.pet_color)
        self.ui.label_105.setText(str(self.current_pet.pet_weight))
        self.ui.label_106.setText(self.current_pet.pet_features)

        # Получаем владельца из БД
        owner = self.owner_repository.get_owner(self.current_pet.owner_id)

        # Звполняем поля формы
        owner_info = f"{owner.owner_lastname} {owner.owner_name} {owner.owner_patronymic}"
        self.ui.label_98.setText(owner_info)
        self.ui.pushButton_17.setText(owner_info)
        self.current_owner_id = self.current_pet.owner_id

        # Загрузка данных о визите
        self.load_visit()

    # Загрузка данных о визите
    def load_visit(self):
        # Получем данные из БД
        last_visit = self.visit_repository.get_visit(self.current_pet.visit_id)
        if last_visit:
            # Если найдено, то заполняем форму данными
            self.ui.label_107.setText(str(last_visit.pet_visit))
            self.ui.label_108.setText(last_visit.pet_complaints)
            self.ui.label_109.setText(last_visit.pet_diagnosis)
            self.ui.label_110.setText(last_visit.pet_analyses)
            self.ui.label_111.setText(last_visit.pet_treatment)
        else:
            # Если не найдено, то ставим прочерки
            self.ui.label_107.setText("-")
            self.ui.label_108.setText("-")
            self.ui.label_109.setText("-")
            self.ui.label_110.setText("-")
            self.ui.label_111.setText("-")

    # Открытие меню редактирования владельца
    def edit_owner(self):
        if self.current_owner_id:
            self.parent.edit_owner.load_owner_data(self.current_owner_id, previous_window=self)
            self.parent.stacked_widget.setCurrentWidget(self.parent.edit_owner)

    # Открытие меню редактирования животного
    def edit_pet(self):
        if self.current_pet_id:
            self.parent.edit_pet.load_pet_data(self.current_pet_id, previous_window=self)
            self.parent.stacked_widget.setCurrentWidget(self.parent.edit_pet)

    # Вернуться в прошлое меню
    def back_to_list(self):
        self.current_pet_id = None
        self.current_pet = None
        self.parent.stacked_widget.setCurrentWidget(self.parent.card_list_menu)

    # Закрыть приложение
    def close_application(self):
        """Закрытие приложения"""
        self.parent.close()
