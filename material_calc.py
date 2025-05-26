from db import get_connection
import math

def calculate_required_material(product_id: int, material_type_id: int, quantity: int, param1: float, param2: float) -> int:
    if quantity <= 0 or param1 <= 0 or param2 <= 0:
        return -1

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT coefficient FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    if not product:
        return -1
    coefficient = product[0]

    cursor.execute("SELECT defect_percentage FROM material_types WHERE type_id = %s", (material_type_id,))
    material_type = cursor.fetchone()
    if not material_type:
        return -1
    defect_percentage = material_type[0]

    conn.close()
#Мы рассчитываем нужное количество материала, умножая два заданных параметра
    # (например, длину и ширину) на коэффициент расхода из изделия,
    # затем умножаем на количество изделий и добавляем запас на брак в процентах —
    # итог округляем вверх до целого.
    base_material = param1 * param2 * coefficient
    total_material = base_material * quantity
    total_with_defect = total_material * (1 + defect_percentage / 100)

    return math.ceil(total_with_defect)
