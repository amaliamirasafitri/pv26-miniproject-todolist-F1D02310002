from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QVBoxLayout
)

class TaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create")

        layout = QVBoxLayout()
        form = QFormLayout()

        # Input
        self.title = QLineEdit()
        self.desc = QTextEdit()

        self.category = QComboBox()
        self.category.addItems(["Kuliah", "Pribadi", "Lainnya"])

        self.priority = QComboBox()
        self.priority.addItems(["Low", "Medium", "High"])

        self.deadline = QLineEdit()

        form.addRow("Title", self.title)
        form.addRow("Desc", self.desc)
        form.addRow("Category", self.category)
        form.addRow("Priority", self.priority)
        form.addRow("Deadline", self.deadline)

        # Button
        btn_save = QPushButton("Save")

        # Untuk simpan data
        btn_save.clicked.connect(self.save_data)

        layout.addLayout(form)
        layout.addWidget(btn_save)
        self.setLayout(layout)

    # Validasi + Accept
    def save_data(self):
        if self.title.text() == "":
            return  # kalau kosong tidak bisa disimpan

        self.accept()

    def get_data(self):
        return (
            self.title.text(),
            self.desc.toPlainText(),
            self.category.currentText(),
            self.priority.currentText(),
            self.deadline.text()
        )