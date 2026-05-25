from typing import Dict, List, Any, Optional

db: Dict[str, List[Dict[str, Any]]] = {
    "customers": [],
    "products": [],
    "orders": []
}

def get_all_customers() -> List[Dict]:
    return db["customers"]

def create_customer(name: str, email: str) -> Dict:
    new_id = len(db["customers"]) + 1
    customer = {"id": new_id, "name": name, "email": email}
    db["customers"].append(customer)
    return customer

def get_all_products() -> List[Dict]:
    return db["products"]

def create_product(name: str, price: float) -> Dict:
    new_id = len(db["products"]) + 1
    product = {"id": new_id, "name": name, "price": price}
    db["products"].append(product)
    return product

def get_all_orders() -> List[Dict]:
    return db["orders"]

def create_order(customer_id: int, product_id: int, quantity: int) -> Optional[Dict]:
    customer_exists = False
    for c in db["customers"]:
        if c["id"] == customer_id:
            customer_exists = True
            break
            
    product_price = 0
    product_exists = False
    for p in db["products"]:
        if p["id"] == product_id:
            product_exists = True
            product_price = p["price"]
            break
            
    if not customer_exists or not product_exists:
        return None
        
    total = product_price * quantity
    new_id = len(db["orders"]) + 1
    
    order = {
        "id": new_id, 
        "customer_id": customer_id, 
        "product_id": product_id, 
        "quantity": quantity, 
        "total": total
    }
    db["orders"].append(order)
    return order