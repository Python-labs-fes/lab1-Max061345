import pytest
from minidb import Database, Column, IntegerType, StringType, FloatType

@pytest.fixture
def db_with_data():
    db = Database("csv_test_db")
    table = db.create_table("products", [
        Column("id", IntegerType(), unique=True),
        Column("name", StringType()),
        Column("price", FloatType())
    ])
    table.insert({"id": 1, "name": "Laptop", "price": 999.50})
    table.insert({"id": 2, "name": "Mouse", "price": 25.00})
    return db, table

def test_csv_export_and_import(db_with_data, tmp_path):
    db, original_table = db_with_data
    
    csv_file = tmp_path / "test_export.csv"
    
    original_table.export_to_csv(str(csv_file))
    assert csv_file.exists()
    
    imported_table = db.create_table("products_imported", [
        Column("id", IntegerType(), unique=True),
        Column("name", StringType()),
        Column("price", FloatType())
    ])
    
    imported_table.import_from_csv(str(csv_file))
    
    assert len(imported_table) == 2
    
    rows = list(imported_table)
    assert rows[0]["name"] == "Laptop"
    assert rows[0]["price"] == 999.50 
    assert rows[1]["name"] == "Mouse"
    assert rows[1]["price"] == 25.00