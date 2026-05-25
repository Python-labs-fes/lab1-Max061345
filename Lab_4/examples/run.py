import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from minidb import Database, Column, IntegerType, StringType, FloatType

def run_demo():
    db = Database("store_db")

    # Створення категорій
    categories_table = db.create_table("categories", [
        Column("id", IntegerType(), unique=True),
        Column("name", StringType(), nullable=False),
    ])
    categories_table.insert({"id": 1, "name": "Smartphones"})
    categories_table.insert({"id": 2, "name": "Laptops"})

    # Створення продуктів із ЗОВНІШНІМ КЛЮЧЕМ (references)
    products_table = db.create_table("products", [
        Column("id", IntegerType(), unique=True),
        # Вказуємо references=("categories", "id") для каскадного видалення
        Column("category_id", IntegerType(), nullable=False, references=("categories", "id")), 
        Column("model", StringType(), nullable=False),
        Column("price", FloatType())
    ])
    
    products_table.insert({"id": 1, "category_id": 1, "model": "iPhone 15", "price": 999.00})
    products_table.insert({"id": 2, "category_id": 1, "model": "Samsung S24", "price": 850.50})
    products_table.insert({"id": 3, "category_id": 2, "model": "MacBook Air", "price": 1200.00})


    print("--- ДО ОНОВЛЕННЯ ---")
    for row in products_table:
        print(row.to_dict())

    # ТЕСТ 1: UPDATE (Оновлення ціни)
    products_table.update(row_id=1, new_data={"price": 899.00, "model": "iPhone 15 (Discount)"})
    print(products_table.get_row({"id": 1}).to_dict())

    # ТЕСТ 2: CASCADING DELETE
    print(f"Кількість товарів до видалення категорії 1: {len(products_table)}")
    
    # Видаляємо категорію Smartphones (id=1)
    categories_table.delete(1)
    
    print(f"Кількість товарів ПІСЛЯ видалення категорії 1: {len(products_table)}")
    print("Залишилися товари:")
    for row in products_table:
        print(row.to_dict())

if __name__ == "__main__":
    run_demo()