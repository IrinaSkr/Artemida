from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui import Ui_createOwner
from db.OwnerRepository import OwnerRepository
from db.models.OwnerDetails import OwnerDetails

# Окно создания владельца
class CreateOwnerWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = Ui_createOwner()
        self.ui.setupUi(self)

        # Определение функционала кнопок
        self.ui.pushButton_2.clicked.connect(self.close_application)
        self.ui.pushButton_3.clicked.connect(self.save_and_back)
        self.ui.pushButton_4.clicked.connect(self.back)
        self.ui.pushButton.clicked.connect(self.back)

        # Создание объектов для общения с БД
        self.owner_repository = OwnerRepository()

# Возврат на прошлое окно (создание карточки животного)
    def back(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.create_pet)

# Сохранить владельца и вернуться к созданию животного
    def save_and_back(self):
        # Получаем данные из формы
        lastname = self.ui.lineEdit_3.text()
        name = self.ui.lineEdit_4.text()
        patronymic = self.ui.lineEdit_5.text()
        phone = self.ui.lineEdit_6.text()
        email = self.ui.lineEdit_7.text()

        # Проверка существования основных полей
        if not lastname or not name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и имя обязательны для заполнения!")
            return

        # Создание владельца в БД
        owner = OwnerDetails(lastname, name, patronymic, phone, email)
        owner = self.owner_repository.create_owner(owner)

        # Передаем данные в форму создания животного
        self.parent.create_pet.set_owner(owner.id, f"{lastname} {name} {patronymic}")
        self.clear_fields()
        self.parent.stacked_widget.setCurrentWidget(self.parent.create_pet)

# Очистить поля формы
    def clear_fields(self):
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_7.clear()

# Закрыть приложение
    def close_application(self):
        self.parent.close()
