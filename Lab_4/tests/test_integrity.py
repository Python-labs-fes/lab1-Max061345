import pytest
from minidb import Database, Column, IntegerType, StringType

@pytest.fixture
def db():
    db = Database("test_db")
    db.create_table("users", [
        Column("id", IntegerType(), unique=True),
        Column("username", StringType(), nullable=False)
    ])
    return db

def test_type_validation(db):
    users = db.get_table("users")
    users.insert({"id": 1, "username": "admin"})
    
    with pytest.raises(TypeError):
        users.insert({"id": 2, "username": 123})

def test_unique_constraint(db):
    users = db.get_table("users")
    users.insert({"id": 1, "username": "admin"})
    
    with pytest.raises(ValueError, match="Unique constraint failed"):
        users.insert({"id": 1, "username": "guest"})

def test_not_null_constraint(db):
    users = db.get_table("users")
    with pytest.raises(ValueError, match="cannot be null"):
        users.insert({"id": 3, "username": None})