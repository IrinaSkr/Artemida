from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui import Ui_CreatePet
from db.PetRepository import PetRepository
from db.VisitRepository import VisitRepository
from db.OwnerRepository import OwnerRepository
from db.models.PetDetails import PetDetails
from db.models.VisitDetails import VisitDetails


# Окно создания новой карты
class CreatePetWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = Ui_CreatePet()
        self.ui.setupUi(self)

        # Определение функционала кнопок
        self.ui.pushButton_7.clicked.connect(self.close_application)
        self.ui.pushButton_6.clicked.connect(self.back_card_list)
        self.ui.pushButton_8.clicked.connect(self.handle_owner)
        self.ui.pushButton_3.clicked.connect(self.save_pet)
        self.ui.pushButton_4.clicked.connect(self.back_main_menu)

        # Добавляем обработчик изменения выбранного владельца
        self.ui.comboBox.currentIndexChanged.connect(self.on_owner_selected)

        # Создание объектов для общения с БД
        self.pet_repository = PetRepository()
        self.visit_repository = VisitRepository()
        self.owner_repository = OwnerRepository()

        # Инициализируем переменные для хранения информации о владельце
        self.current_owner_id = None
        self.current_owner_name = None

    # Метод который вызывается при открытии окна и обновляет данные в таблице
    def showEvent(self, event):
        self.load_owners()
        super().showEvent(event)

    def load_owners(self):
        # Получаем всех владельцев
        owners = self.owner_repository.get_all_owners()

        # Очищаем выпадающий список
        self.ui.comboBox.clear()

        # Добавляем владельцев в выпадающий список
        self.ui.comboBox.addItem("Выбрать", None)
        for owner in owners:
            # Формируем строку для отображения (фамилия, имя, отчество)
            display_text = f"{owner.owner_lastname} {owner.owner_name} {owner.owner_patronymic}"
            # Добавляем в выпадающий список
            self.ui.comboBox.addItem(display_text, owner.id)

    def save_pet(self):
        # Проверка что владелец указан
        if not self.current_owner_id:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите владельца!")
            return

        # Получаем данные с формы
        pet_name = self.ui.lineEdit_2.text()
        pet_type = self.ui.lineEdit_11.text()
        pet_sex = self.ui.lineEdit_12.text()
        pet_birthday = self.ui.lineEdit_13.text()
        pet_age = self.ui.lineEdit_14.text()
        pet_breed = self.ui.lineEdit_15.text()
        pet_color = self.ui.lineEdit_16.text()
        pet_weight = self.ui.lineEdit_17.text()
        pet_features = self.ui.lineEdit_18.text()

        # Проверка на существование основных полец
        if not pet_name or not pet_type:
            QMessageBox.warning(self, "Ошибка", "Кличка и вид животного обязательны для заполнения!")
            return

        # Сохраняем визит
        visit = self.save_visit()

        # Сохраняем животного
        pet = PetDetails(
            owner_id=self.current_owner_id,
            pet_name=pet_name,
            pet_type=pet_type,
            pet_sex=pet_sex,
            pet_birthday=pet_birthday,
            pet_age=pet_age,
            pet_breed=pet_breed,
            pet_color=pet_color,
            pet_weight=pet_weight,
            pet_features=pet_features,
            pet_visit=visit.pet_visit,
            visit_id=visit.id
        )
        self.pet_repository.create_pet(pet)

        self.clear_fields()
        self.back_main_menu()

    # Сохранение визита
    def save_visit(self):
        visit = VisitDetails(
            pet_visit=self.ui.lineEdit_23.text(),
            pet_complaints=self.ui.lineEdit_24.text(),
            pet_diagnosis=self.ui.lineEdit_25.text(),
            pet_analyses=self.ui.textEdit_4.toPlainText(),
            pet_treatment=self.ui.textEdit_3.toPlainText()
        )
        return self.visit_repository.create_visit(visit)

    # Очистка полей формы
    def clear_fields(self):
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_11.clear()
        self.ui.lineEdit_12.clear()
        self.ui.lineEdit_13.clear()
        self.ui.lineEdit_14.clear()
        self.ui.lineEdit_15.clear()
        self.ui.lineEdit_16.clear()
        self.ui.lineEdit_17.clear()
        self.ui.lineEdit_18.clear()
        self.ui.lineEdit_23.clear()
        self.ui.lineEdit_24.clear()
        self.ui.lineEdit_25.clear()
        self.ui.textEdit_3.clear()
        self.ui.textEdit_4.clear()
        self.current_owner_id = None
        self.current_owner_name = None

    # Возврат назад по меню
    def back_card_list(self):
        self.current_owner_id = None
        self.current_owner_name = None
        self.clear_fields()
        self.parent.stacked_widget.setCurrentWidget(self.parent.card_list_menu)

    def back_main_menu(self):
        self.current_owner_id = None
        self.current_owner_name = None
        self.clear_fields()
        self.parent.stacked_widget.setCurrentWidget(self.parent.main_menu)

    # Выбор формы (изменение или создание владельца)
    def handle_owner(self):
        # Открываем окно создания владельца
        self.parent.stacked_widget.setCurrentWidget(self.parent.create_owner)

    # При выборе владельца из списка сохраняем его ID
    def on_owner_selected(self, index):
        if index >= 0:
            # Получаем ID владельца из данных элемента
            self.current_owner_id = self.ui.comboBox.itemData(index)
            self.current_owner_name = self.ui.comboBox.currentText()

    def close_application(self):
        self.parent.close()
