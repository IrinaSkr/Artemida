from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QMessageBox
from ui import Ui_cardList
from db.PetRepository import PetRepository
from db.OwnerRepository import OwnerRepository
from windows.DeleteDialog import DeleteDialog


# Окно списка карточек
class CardListWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = Ui_cardList()
        self.ui.setupUi(self)
        # Подключаем функционал к кнопкам
        self.ui.pushButton.clicked.connect(self.back_main_menu)
        self.ui.pushButton_2.clicked.connect(self.close_application)
        self.ui.pushButton_3.clicked.connect(self.show_create_pet)
        self.ui.pushButton_4.clicked.connect(self.delete_pet)

        # Создаем классы для общения с БД
        self.pet_repository = PetRepository()
        self.owner_repository = OwnerRepository()

        # Настройка таблицы
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрет редактирования
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделение строк
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)  # Выделение только одной строки
        self.ui.tableWidget.doubleClicked.connect(self.open_pet_card)  # Обработка двойного клика на открытие карточки

    # Удаление питомца
    def delete_pet(self):
        current_row = self.ui.tableWidget.currentRow()
        # Проверка выбрана ли строка
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите питомца для удаления!")
            return

        pet_id = int(self.ui.tableWidget.item(current_row, 0).text())

        # Вызов диалога на удаление
        dialog = DeleteDialog(self)
        if dialog.exec_() == DeleteDialog.Accepted:
            self.pet_repository.delete_pet(pet_id)
            self.load_data_to_table()

    # Метод который вызывается при открытии окна и обновляет данные в таблице
    def showEvent(self, event):
        self.load_data_to_table()
        super().showEvent(event)

    # Загрузка данных в таблицу
    def load_data_to_table(self):
        # Получаем всех животных из БД
        pets = self.pet_repository.get_all_pets()
        self.ui.tableWidget.setRowCount(len(pets))

        # Добавляем животных в таблицу
        for row, pet in enumerate(pets):
            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(pet.id)))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(pet.pet_name))
            owner = self.owner_repository.get_owner(pet.owner_id)
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(
                f"{owner.owner_lastname} {owner.owner_name} {owner.owner_patronymic}"))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(pet.id)))

    # Открытие карточки животного
    def open_pet_card(self):
        current_row = self.ui.tableWidget.currentRow()
        if current_row >= 0:
            pet_id = int(self.ui.tableWidget.item(current_row, 0).text())
            self.parent.pet_card.load_pet_data(pet_id)
            self.parent.stacked_widget.setCurrentWidget(self.parent.pet_card)

    # Возврат в главное меню
    def back_main_menu(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.main_menu)

    # Открытие формы на создание животного
    def show_create_pet(self):
        self.parent.create_pet.clear_fields()
        self.parent.stacked_widget.setCurrentWidget(self.parent.create_pet)

    # Закрыть приложение
    def close_application(self):
        self.parent.close()