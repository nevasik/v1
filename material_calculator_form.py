from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
)
from material_calc import calculate_required_material
from db import get_connection

class MaterialCalculatorForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Расчёт необходимого материала")
        self.layout = QVBoxLayout(self)

        self.product_combo = QComboBox()
        self.material_combo = QComboBox()
        self.quantity_input = QLineEdit()
        self.param1_input = QLineEdit()
        self.param2_input = QLineEdit()

        self.layout.addWidget(QLabel("Тип продукции"))
        self.layout.addWidget(self.product_combo)
        self.layout.addWidget(QLabel("Тип материала"))
        self.layout.addWidget(self.material_combo)
        self.layout.addWidget(QLabel("Количество продукции"))
        self.layout.addWidget(self.quantity_input)
        self.layout.addWidget(QLabel("Параметр 1"))
        self.layout.addWidget(self.param1_input)
        self.layout.addWidget(QLabel("Параметр 2"))
        self.layout.addWidget(self.param2_input)

        self.load_data()

        btn_calc = QPushButton("Рассчитать")
        btn_calc.clicked.connect(self.calculate)
        self.layout.addWidget(btn_calc)

    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT product_id, name FROM products")
        for pid, name in cursor.fetchall():
            self.product_combo.addItem(name, pid)

        cursor.execute("SELECT type_id, name FROM material_types")
        for tid, name in cursor.fetchall():
            self.material_combo.addItem(name, tid)

        conn.close()

    def calculate(self):
        try:
            product_id = self.product_combo.currentData()
            material_type_id = self.material_combo.currentData()
            quantity = int(self.quantity_input.text())
            param1 = float(self.param1_input.text())
            param2 = float(self.param2_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Проверьте введённые данные.")
            return

        result = calculate_required_material(product_id, material_type_id, quantity, param1, param2)

        if result == -1:
            QMessageBox.critical(self, "Ошибка", "Некорректные данные для расчёта.")
        else:
            QMessageBox.information(self, "Результат", f"Необходимое количество материала: {result}")
