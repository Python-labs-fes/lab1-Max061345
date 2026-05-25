from typing import Any, Tuple, Dict

def validate_email(email: str) -> Tuple[bool, str]:
    if type(email) is str and "@" in email and "." in email:
        return True, ""
    return False, "Невірний формат email"

def validate_positive_number(value: Any) -> Tuple[bool, str]:
    if type(value) in (int, float) and value > 0:
        return True, ""
    return False, "Значення має бути додатним числом"

def validate_customer_input(data: Dict) -> Tuple[bool, str]:
    if "name" not in data or not data["name"]:
        return False, "Ім'я є обов'язковим"
    if "email" not in data:
        return False, "Email є обов'язковим"
    
    is_valid_email, msg = validate_email(data["email"])
    if not is_valid_email:
        return False, msg
        
    return True, ""

def validate_product_input(data: Dict) -> Tuple[bool, str]:
    if "name" not in data or not data["name"]:
        return False, "Назва продукту є обов'язковою"
    if "price" not in data:
        return False, "Ціна є обов'язковою"
        
    is_valid_price, msg = validate_positive_number(data["price"])
    if not is_valid_price:
        return False, msg
        
    return True, ""

def validate_order_input(data: Dict) -> Tuple[bool, str]:
    if type(data.get("customer_id")) is not int:
        return False, "customer_id має бути цілим числом"
    if type(data.get("product_id")) is not int:
        return False, "product_id має бути цілим числом"
    if type(data.get("quantity")) is not int or data.get("quantity") <= 0:
        return False, "quantity має бути додатним цілим числом"
    
    return True, ""