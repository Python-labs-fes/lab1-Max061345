import pytest
from minidb import Database, Column, IntegerType, StringType

@pytest.fixture
def db_with_relations():
    """Фікстура, що створює базу з двома пов'язаними таблицями для тестування CRUD та каскаду."""
    db = Database("test_crud_db")
    
    categories = db.create_table("categories", [
        Column("id", IntegerType(), unique=True),
        Column("name", StringType(), nullable=False)
    ])
    
    products = db.create_table("products", [
        Column("id", IntegerType(), unique=True),
        # Налаштовуємо зовнішній ключ для перевірки каскадного видалення
        Column("category_id", IntegerType(), references=("categories", "id")),
        Column("name", StringType())
    ])
    
    # Наповнюємо даними
    categories.insert({"id": 1, "name": "Electronics"})
    categories.insert({"id": 2, "name": "Clothing"})
    
    products.insert({"id": 1, "category_id": 1, "name": "Laptop"})
    products.insert({"id": 2, "category_id": 1, "name": "Smartphone"})
    products.insert({"id": 3, "category_id": 2, "name": "T-Shirt"})
    
    return db, categories, products

def test_update_row(db_with_relations):
    """Тестує успішне оновлення рядка."""
    _, categories, _ = db_with_relations
    
    # Оновлюємо назву категорії
    updated_row = categories.update(1, {"name": "Tech Gadgets"})
    
    assert updated_row is not None
    assert updated_row["name"] == "Tech Gadgets"
    
    # Перевіряємо, що зміни збереглися в самій таблиці
    fetched_row = categories.get_row({"id": 1})
    assert fetched_row["name"] == "Tech Gadgets"

def test_update_validation_rollback(db_with_relations):
    """Тестує, що при помилці валідації під час оновлення, старі дані не псуються."""
    _, categories, _ = db_with_relations
    
    # Намагаємося оновити рядок невалідним типом (int замість string)
    with pytest.raises(TypeError):
        categories.update(1, {"name": 12345})
        
    # Перевіряємо, що після помилки рядок не зник і зберіг старі дані
    row = categories.get_row({"id": 1})
    assert row is not None
    assert row["name"] == "Electronics"

def test_delete_row_simple(db_with_relations):
    """Тестує звичайне видалення рядка."""
    _, categories, _ = db_with_relations
    
    # Видаляємо категорію "Clothing", у якої лише 1 товар
    categories.delete(2)
    
    assert len(categories) == 1
    assert categories.get_row({"id": 2}) is None

def test_cascading_delete(db_with_relations):
    """Тестує каскадне видалення зв'язаних рядків."""
    _, categories, products = db_with_relations
    
    assert len(products) == 3
    
    # Видаляємо категорію 1 (Electronics). Це має автоматично видалити Laptop та Smartphone
    categories.delete(1, cascade=True)
    
    # Перевіряємо таблицю категорій
    assert len(categories) == 1
    assert categories.get_row({"id": 1}) is None
    
    # Перевіряємо таблицю продуктів
    assert len(products) == 1
    
    # Має залишитися тільки футболка (T-Shirt), бо вона належить до категорії 2
    remaining_product = products.get_row({"id": 3})
    assert remaining_product is not None
    assert remaining_product["name"] == "T-Shirt"