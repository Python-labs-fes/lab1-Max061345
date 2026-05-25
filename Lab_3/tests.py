import pytest
from framework import app, _routes
from main import dispatch
from middleware import transaction_log
from models import db
import importlib
import views

def reset_state():
    """Скидає глобальний стан для забезпечення ізоляції тестів."""
    transaction_log.clear()
    _routes.clear()
    
    # Скидання Бази Даних
    db["customers"] = []
    db["products"] = []
    db["orders"] = []
    
    # Перезавантаження views для заповнення реєстру _routes
    importlib.reload(views)

def test_route_registration_integrity():
    """Перевіряє, що декоратори правильно реєструють шляхи у фреймворку."""
    reset_state()
    assert ('GET', '/customers') in _routes
    assert ('POST', '/orders') in _routes

def test_validation_email_format():
    """Перевіряє, що створення Клієнта не вдається з невірним email."""
    reset_state()
    request = {
        "method": "POST",
        "path": "/customers",
        "session": {"user_id": 1, "role": "admin"},
        "body": {"name": "test name", "email": "invalid-email"},
        "query": {}
    }
    response = dispatch(request)
    assert response['status_code'] == 400
    assert len(db["customers"]) == 0

def test_validation_positive_price():
    """Перевіряє, що створення Продукту не вдається з від'ємною ціною."""
    reset_state()
    request = {
        "method": "POST",
        "path": "/products",
        "session": {"user_id": 1, "role": "admin"},
        "body": {"name": "Laptop", "price": -100},
        "query": {}
    }
    response = dispatch(request)
    assert response['status_code'] == 400
    assert len(db["products"]) == 0

def test_relational_integrity_valid_order():
    """Перевіряє, що створення Замовлення вдається з valid ID."""
    reset_state()
    db["customers"].append({"id": 1, "name": "test name", "email": "a@test.com"})
    db["products"].append({"id": 1, "name": "Laptop", "price": 1000})
    
    request = {
        "method": "POST",
        "path": "/orders",
        "session": {"user_id": 1, "role": "user"},
        "body": {"customer_id": 1, "product_id": 1, "quantity": 2},
        "query": {}
    }
    response = dispatch(request)
    assert response['status_code'] == 201
    assert len(db["orders"]) == 1
    assert db["orders"][0]["total"] == 2000

def test_relational_integrity_invalid_order():
    """Перевіряє, що створення Замовлення не вдається з невірними ID."""
    reset_state()
    request = {
        "method": "POST",
        "path": "/orders",
        "session": {"user_id": 1, "role": "user"},
        "body": {"customer_id": 999, "product_id": 999, "quantity": 1},
        "query": {}
    }
    response = dispatch(request)
    assert response['status_code'] == 400
    assert len(db["orders"]) == 0

def test_audit_log_capture_relational():
    """Перевіряє, що audit_log записує операції Замовлення."""
    reset_state()
    db["customers"].append({"id": 1, "name": "test name", "email": "a@test.com"})
    db["products"].append({"id": 1, "name": "Laptop", "price": 1000})
    
    request = {
        "method": "POST",
        "path": "/orders",
        "session": {"user_id": 1, "role": "user"},
        "body": {"customer_id": 1, "product_id": 1, "quantity": 1},
        "query": {}
    }
    dispatch(request)
    
    assert len(transaction_log) == 1
    entry = transaction_log[0]
    assert entry['path'] == '/orders'
    assert entry['status_code'] == 201