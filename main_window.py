### main_window.py
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox)
from Material_form import MaterialForm
from db import get_connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(500,200)
        self.setWindowTitle("Склад материалов")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color:white")
        self.setFont(QFont("Bahnschrift Light SemiCondensed"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Ед.", "Остаток", "Тип"])
        self.table.cellDoubleClicked.connect(self.edit_material)
        layout.addWidget(self.table)

        btn_add = QPushButton("Добавить материал")
        btn_add.setStyleSheet("background-color:blue")
        btn_add.clicked.connect(self.add_material)
        layout.addWidget(btn_add)

        btn_suppliers = QPushButton("Просмотр поставщиков материала")

        btn_suppliers.setStyleSheet("background-color:blue")
        btn_suppliers.clicked.connect(self.view_material_suppliers)
        layout.addWidget(btn_suppliers)

        central_widget.setLayout(layout)
        self.load_materials()

    def load_materials(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.material_id, m.name, m.unit, m.stock_quantity, t.name
            FROM materials m
            JOIN material_types t ON m.type_id = t.type_id
        """)
        materials = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(materials))
        for row, material in enumerate(materials):
            for col, value in enumerate(material):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_material(self):
        form = MaterialForm(parent=self)
        if form.exec():
            self.load_materials()

    def edit_material(self, row, column):
        material_id = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        unit = self.table.item(row, 2).text()
        stock_quantity = float(self.table.item(row, 3).text())
        type_name = self.table.item(row, 4).text()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT type_id FROM material_types WHERE name = %s", (type_name,))
        type_id = cursor.fetchone()[0]
        conn.close()

        material = (material_id, name, unit, stock_quantity, type_id)
        form = MaterialForm(material=material, parent=self)
        if form.exec():
            self.load_materials()

    def view_material_suppliers(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.information(self, "Выбор материала", "Пожалуйста, выберите материал")
            return

        material_id = int(self.table.item(selected_row, 0).text())
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.name, s.contact_info
            FROM suppliers s
            JOIN material_suppliers ms ON s.supplier_id = ms.supplier_id
            WHERE ms.material_id = %s
        """, (material_id,))
        suppliers = cursor.fetchall()
        conn.close()

        if not suppliers:
            QMessageBox.information(self, "Поставщики", "Для выбранного материала нет поставщиков.")
            return

        text = "\n".join([f"{name} ({info})" for name, info in suppliers])
        QMessageBox.information(self, "Поставщики материала", text)
