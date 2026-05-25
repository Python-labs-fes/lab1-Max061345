import pytest
from minidb import Database, Column, IntegerType, StringType

@pytest.fixture
def populate_db():
    db = Database("query_test_db")
    users = db.create_table("users", [
        Column("id", IntegerType()),
        Column("age", IntegerType()),
        Column("department", StringType())
    ])
    users.insert({"id": 1, "department": "IT", "age": 25})
    users.insert({"id": 2, "department": "IT", "age": 35})
    users.insert({"id": 3, "department": "HR", "age": 30})
    return users

def test_simple_select_where(populate_db):
    users = populate_db
    result = users.query().where("age", ">", 28).execute()
    assert len(result) == 2

def test_method_chaining(populate_db):
    users = populate_db
    result = (users.query()
              .select(["department"])
              .order_by("age", ascending=False)
              .limit(1)
              .execute())
    assert len(result) == 1
    assert result[0] == {"department": "IT"} 

def test_aggregation_sum_and_avg(populate_db):
    users = populate_db
    assert users.query().sum("age") == 90
    
    assert users.query().avg("age") == 30.0

def test_aggregation_group_by(populate_db):
    users = populate_db
    
    counts = users.query().group_by("department").count()
    assert counts == {"IT": 2, "HR": 1}
    
    averages = users.query().group_by("department").avg("age")
    assert averages == {"IT": 30.0, "HR": 30.0}