from typing import Dict, Any
from framework import app
from middleware import audit_log, login_required, role_required
import models
import validators
from templates import render_json, render_error

@app.get("/customers")
@audit_log
@login_required
def list_customers(request: Dict[str, Any]) -> Dict[str, Any]:
    data = models.get_all_customers()
    return {
        "status_code": 200,
        "body": render_json(data),
        "headers": {"Content-Type": "application/json"}
    }

@app.post("/customers")
@audit_log
@login_required
@role_required("admin")
def add_customer(request: Dict[str, Any]) -> Dict[str, Any]:
    body = request.get("body", {})
    
    is_valid, error_msg = validators.validate_customer_input(body)
    if not is_valid:
        return {"status_code": 400, "body": render_error(error_msg), "headers": {}}
        
    new_customer = models.create_customer(body["name"], body["email"])
    return {
        "status_code": 201,
        "body": render_json(new_customer),
        "headers": {"Content-Type": "application/json"}
    }

@app.get("/products")
@audit_log
def list_products(request: Dict[str, Any]) -> Dict[str, Any]:
    data = models.get_all_products()
    return {
        "status_code": 200,
        "body": render_json(data),
        "headers": {"Content-Type": "application/json"}
    }

@app.post("/products")
@audit_log
@login_required
@role_required("admin")
def add_product(request: Dict[str, Any]) -> Dict[str, Any]:
    body = request.get("body", {})
    
    is_valid, error_msg = validators.validate_product_input(body)
    if not is_valid:
        return {"status_code": 400, "body": render_error(error_msg), "headers": {}}
        
    new_product = models.create_product(body["name"], body["price"])
    return {
        "status_code": 201,
        "body": render_json(new_product),
        "headers": {"Content-Type": "application/json"}
    }

@app.post("/orders")
@audit_log
@login_required
def make_order(request: Dict[str, Any]) -> Dict[str, Any]:
    body = request.get("body", {})
    
    is_valid, error_msg = validators.validate_order_input(body)
    if not is_valid:
        return {"status_code": 400, "body": render_error(error_msg), "headers": {}}
        
    order = models.create_order(
        customer_id=body["customer_id"],
        product_id=body["product_id"],
        quantity=body["quantity"]
    )
    
    if order is None:
        return {"status_code": 400, "body": render_error("Клієнт або продукт не знайдено"), "headers": {}}
        
    return {
        "status_code": 201,
        "body": render_json(order),
        "headers": {"Content-Type": "application/json"}
    }

@app.get("/orders")
@audit_log
@login_required
@role_required("admin")
def list_orders(request: Dict[str, Any]) -> Dict[str, Any]:
    data = models.get_all_orders()
    return {
        "status_code": 200,
        "body": render_json(data),
        "headers": {"Content-Type": "application/json"}
    }