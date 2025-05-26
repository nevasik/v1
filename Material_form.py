from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
)
from db import get_connection

class MaterialForm(QDialog):
    def __init__(self, material=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать материал" if material else "Добавить материал")
        self.material = material
        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.stock_input = QLineEdit()
        self.price_input = QLineEdit()
        self.type_combo = QComboBox()
        self.supplier_combo = QComboBox()

        self.layout.addWidget(QLabel("Название"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Ед. измерения"))
        self.layout.addWidget(self.unit_input)
        self.layout.addWidget(QLabel("Остаток"))
        self.layout.addWidget(self.stock_input)
        self.layout.addWidget(QLabel("Цена за единицу"))
        self.layout.addWidget(self.price_input)
        self.layout.addWidget(QLabel("Тип материала"))
        self.layout.addWidget(self.type_combo)
        self.layout.addWidget(QLabel("Поставщик"))
        self.layout.addWidget(self.supplier_combo)

        try:
            self.load_types()
            self.load_suppliers()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Не удалось загрузить данные: {e}")
            self.reject()
            return

        if material:
            self.name_input.setText(material[1])
            self.unit_input.setText(material[2])
            self.stock_input.setText(str(material[3]))
            self.price_input.setText(str(material[5]))
            self.type_combo.setCurrentIndex(self.find_type_index(material[4]))
            self.supplier_combo.setCurrentIndex(0)

        btn_save = QPushButton("Сохранить")
        btn_save.clicked.connect(self.save_material)
        self.layout.addWidget(btn_save)
        self.setLayout(self.layout)

    def load_types(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT type_id, name FROM material_types")
        self.types = cursor.fetchall()
        conn.close()
        for t in self.types:
            self.type_combo.addItem(t[1], t[0])

    def find_type_index(self, type_id):
        for index, (tid, _) in enumerate(self.types):
            if tid == type_id:
                return index
        return 0

    def load_suppliers(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT supplier_id, name FROM suppliers")
        self.suppliers = cursor.fetchall()
        conn.close()
        for s in self.suppliers:
            self.supplier_combo.addItem(s[1], s[0])

    def save_material(self):
        name = self.name_input.text().strip()
        unit = self.unit_input.text().strip()

        try:
            stock = float(self.stock_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректное значение остатка. Введите число.")
            return

        try:
            price = float(self.price_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректное значение цены. Введите число.")
            return

        type_id = self.type_combo.currentData()
        supplier_id = self.supplier_combo.currentData()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название материала.")
            return
        if not unit:
            QMessageBox.warning(self, "Ошибка", "Введите единицу измерения.")
            return
        if type_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите тип материала.")
            return
        if supplier_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите поставщика.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            if self.material:
                cursor.execute("""
                    UPDATE materials
                    SET name=%s, unit=%s, stock_quantity=%s, type_id=%s, price_per_unit=%s
                    WHERE material_id=%s
                """, (name, unit, stock, type_id, price, self.material[0]))
            else:
                cursor.execute("""
                    INSERT INTO materials (name, unit, stock_quantity, type_id, price_per_unit)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, unit, stock, type_id, price))
                material_id = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO material_suppliers (material_id, supplier_id)
                    VALUES (%s, %s)
                """, (material_id, supplier_id))

            conn.commit()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Произошла ошибка:\n{str(e)}")
            return
        finally:
            conn.close()

        self.accept()
