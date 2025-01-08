from PyQt5.QtWidgets import QDialog
from ui import Ui_Dialog


# Диалоговое окно на удаление
class DeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Подключаем кнопки
        self.ui.pushButton_3.clicked.connect(self.accept)  # Кнопка "Да"
        self.ui.pushButton_4.clicked.connect(self.reject)  # Кнопка "Нет"
