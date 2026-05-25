from main import dispatch
import views 
import models

models.db["products"].append({"id": 1, "name": "Ноутбук", "price": 25000})


request_get_products = {
    "method": "GET",
    "path": "/products",
    "session": {}, 
    "body": {},
    "query": {}
}

# 3. Відправляємо запит у наш "фреймворк"
print("Відправляємо запит на /products")
response = dispatch(request_get_products)
print("Відповідь:", response)



request_get_orders = {
    "method": "GET",
    "path": "/orders",
    "session": {}, 
    "body": {},
    "query": {}
}

print("\nВідправляємо запит на /orders без авторизації")
response_orders = dispatch(request_get_orders)
print("Відповідь:", response_orders)