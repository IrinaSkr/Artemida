import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from windows.CardListWindow import CardListWindow
from windows.MainWindow import MainWindow
from windows.CreatePetWindow import CreatePetWindow
from windows.CreateOwnerWindow import CreateOwnerWindow
from windows.EditOwnerWindow import EditOwnerWindow
from windows.PetCardWindow import PetCardWindow
from windows.EditPetWindow import EditPetWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1440, 864)
        self.setWindowTitle("Артемида")

        # Создаем стек виджетов, куда поместим все окна для удобного переключения
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Создаем окна
        self.main_menu = MainWindow(self)
        self.card_list_menu = CardListWindow(self)
        self.create_pet = CreatePetWindow(self)
        self.create_owner = CreateOwnerWindow(self)
        self.edit_owner = EditOwnerWindow(self)
        self.pet_card = PetCardWindow(self)
        self.edit_pet = EditPetWindow(self)

        # Добавляем окна в стек
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.card_list_menu)
        self.stacked_widget.addWidget(self.create_pet)
        self.stacked_widget.addWidget(self.create_owner)
        self.stacked_widget.addWidget(self.edit_owner)
        self.stacked_widget.addWidget(self.pet_card)
        self.stacked_widget.addWidget(self.edit_pet)

        # Включаем главное окно
        self.stacked_widget.setCurrentWidget(self.main_menu)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())