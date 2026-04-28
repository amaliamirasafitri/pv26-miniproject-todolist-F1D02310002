from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QHBoxLayout, QMessageBox,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PySide6.QtCore import Qt

from database.db import Database
from ui.task_dialog import TaskDialog

class MainWindow(QMainWindow):
    def __init__(self, username="User"):
        super().__init__()
        self.setWindowTitle("To-Do List App")
        self.resize(800, 600)

        self.db = Database()
        self.username = username

        central = QWidget()
        layout = QVBoxLayout()

        # ================= MENU =================
        menu_bar = self.menuBar()
        menu_info = menu_bar.addMenu("About The Application")

        about_action = menu_info.addAction("Show Application")
        about_action.triggered.connect(self.show_about)

        # ================= HEADER =================
        header = QWidget()
        header.setObjectName("header")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("To Do List App")
        title.setObjectName("title")

        user_label = QLabel(f"Hi, {self.username} 👋")
        user_label.setObjectName("userLabel")

        btn_logout = QPushButton("Logout")
        btn_logout.setObjectName("btnLogout")
        btn_logout.clicked.connect(self.logout)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(user_label)
        header_layout.addWidget(btn_logout)

        header.setLayout(header_layout)
        layout.addWidget(header)

        # ================= SEARCH =================
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search task...")
        self.search_input.textChanged.connect(self.load_data)

        self.filter_priority = QComboBox()
        self.filter_priority.addItems(["All", "Low", "Medium", "High"])
        self.filter_priority.currentTextChanged.connect(self.load_data)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.filter_priority)

        layout.addLayout(search_layout)

        # ================= TABLE =================
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "No", "Judul", "Kategori", "Prioritas", "Status", "Aksi"
        ])

        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)

        self.table.setStyleSheet("""
        QTableWidget {
            gridline-color: #ccc;
            background-color: white;
        }

        QHeaderView::section {
            background-color: #1c7ed6;
            color: white;
            padding: 5px;
            border: none;
        }
        """)

        # Kolom normal stretch
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Kolom AKSI agar tombol rapi
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(5, 190)

        layout.addWidget(self.table)

        # ================= BUTTON CREATE =================
        self.btn_add = QPushButton("Create")
        self.btn_add.setObjectName("btnAdd")
        self.btn_add.clicked.connect(self.open_dialog)
        layout.addWidget(self.btn_add)

        central.setLayout(layout)
        self.setCentralWidget(central)

        self.load_data()

    # ================= ABOUT =================
    def show_about(self):
        QMessageBox.information(
            self,
            "About Application",
            "To-Do List App\n\n"
            "Aplikasi To-Do List App merupakan aplikasi manajemen tugas berbasis desktop yang dikembangkan menggunakan library PySide6 pada bahasa pemrograman Python. Aplikasi ini dirancang untuk membantu pengguna dalam mencatat, mengelola, serta memantau daftar tugas sehari-hari secara terstruktur dan efisien.\n\n"
            "Nama : AMALIA MIRASAFITRI\n"
            "NIM    : F1D02310002"
        )

    # ================= LOAD DATA =================
    def load_data(self):
        self.table.setRowCount(0)
        data = self.db.get_tasks()

        keyword = self.search_input.text().strip().lower()
        priority_filter = self.filter_priority.currentText()

        no = 1

        for task in data:
            task_id, title, desc, cat, priority, deadline, status = task

            title_text = (title or "").lower()
            desc_text = (desc or "").lower()

            if keyword:
                if keyword not in title_text and keyword not in desc_text:
                    continue

            if priority_filter != "All":
                if priority != priority_filter:
                    continue

            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(no)))
            self.table.setItem(row, 1, QTableWidgetItem(title))
            self.table.setItem(row, 2, QTableWidgetItem(cat))
            self.table.setItem(row, 3, QTableWidgetItem(priority))
            self.table.setItem(row, 4, QTableWidgetItem(status))

            no += 1 # Supaya nomor urut tidak double

            # ================= AKSI BUTTON =================
            action_widget = QWidget()

            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(8, 2, 8, 2)
            action_layout.setSpacing(6)
            action_layout.setAlignment(Qt.AlignCenter)

            btn_edit = QPushButton("Update")
            btn_edit.setObjectName("btnEdit")
            btn_edit.setFixedSize(75, 28)

            btn_delete = QPushButton("Delete")
            btn_delete.setObjectName("btnDelete")
            btn_delete.setFixedSize(75, 28)

            btn_edit.clicked.connect(
                lambda _, id=task_id: self.edit_task(id)
            )

            btn_delete.clicked.connect(
                lambda _, id=task_id: self.delete_task(id)
            )

            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)

            self.table.setCellWidget(row, 5, action_widget)

    # ================= TAMBAH =================
    def open_dialog(self):
        dialog = TaskDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.db.add_task(data)
            QMessageBox.information(self, "Success", "Data added")
            self.load_data()

    # ================= EDIT =================
    def edit_task(self, task_id):
        data = self.db.get_tasks()

        for task in data:
            if task[0] == task_id:
                dialog = TaskDialog(self)

                dialog.title.setText(task[1])
                dialog.desc.setText(task[2])
                dialog.category.setCurrentText(task[3])
                dialog.priority.setCurrentText(task[4])
                dialog.deadline.setText(task[5])

                if dialog.exec():
                    new_data = dialog.get_data()
                    self.db.update_task(task_id, new_data)
                    QMessageBox.information(self, "Success", "Updated")
                    self.load_data()
                break

    # ================= DELETE =================
    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self.load_data()

    # ================= LOGOUT =================
    def logout(self):
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()