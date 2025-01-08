from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui import Ui_editOwner
from db.OwnerRepository import OwnerRepository
from db.models.OwnerDetails import OwnerDetails

# Окно редактирования владельца
class EditOwnerWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = Ui_editOwner()
        self.ui.setupUi(self)

        # Определение функционала кнопок
        self.ui.pushButton_2.clicked.connect(self.close_application)
        self.ui.pushButton_6.clicked.connect(self.save_and_back)
        self.ui.pushButton_7.clicked.connect(self.back_to_previous)
        self.ui.pushButton.clicked.connect(self.back_to_previous)

        # Создание объектов для работы окна
        self.current_owner_id = None
        self.owner_repository = OwnerRepository()
        self.previous_window = None

# Загрузка данный владельца
    def load_owner_data(self, owner_id, previous_window=None):
        self.current_owner_id = owner_id
        # Предыдущее открытое окно (форма может открываться из 2 мест, создание и редактирование животного)
        self.previous_window = previous_window or self.parent.create_pet
        # Поиск владельца в базе
        owner = self.owner_repository.get_owner(owner_id)
        # Заполнение данных в форме
        self.ui.lineEdit_3.setText(owner.owner_lastname)
        self.ui.lineEdit_4.setText(owner.owner_name)
        self.ui.lineEdit_5.setText(owner.owner_patronymic)
        self.ui.lineEdit_6.setText(owner.owner_phone)
        self.ui.lineEdit_7.setText(owner.owner_email)
        self.ui.label_7.setText(f"{owner.owner_lastname} {owner.owner_name} {owner.owner_patronymic}")

# Вернуться в предыдущее меню
    def back_to_previous(self):
        if self.previous_window:
            self.parent.stacked_widget.setCurrentWidget(self.previous_window)
        else:
            self.parent.stacked_widget.setCurrentWidget(self.parent.create_pet)
        self.current_owner_id = None
        self.previous_window = None
        self.clear_fields()

    # Очистка полей формы
    def clear_fields(self):
        self.ui.lineEdit_3.setText("")
        self.ui.lineEdit_4.setText("")
        self.ui.lineEdit_5.setText("")
        self.ui.lineEdit_6.setText("")
        self.ui.lineEdit_7.setText("")
        self.ui.label_7.setText("")


# Сохранить владельца и вернуться в прошлое меню
    def save_and_back(self):
        # Получение данных с формы
        lastname = self.ui.lineEdit_3.text()
        name = self.ui.lineEdit_4.text()
        patronymic = self.ui.lineEdit_5.text()
        phone = self.ui.lineEdit_6.text()
        email = self.ui.lineEdit_7.text()

        # Проверка что основные поля заполнены
        if not lastname or not name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и имя обязательны для заполнения!")
            return

        # Обновляем данные владельца в БД
        owner = OwnerDetails(lastname, name, patronymic, phone, email, self.current_owner_id)
        self.owner_repository.update_owner(owner)

        # Обновляем информацию в окне создания питомца
        self.parent.create_pet.set_owner(
            self.current_owner_id,
            f"{lastname} {name} {patronymic}"
        )

        # Возвращаемся к предыдущему окну
        self.back_to_previous()

# Закрыть приложение
    def close_application(self):
        self.parent.close()
