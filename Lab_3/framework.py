from types import SimpleNamespace
from typing import Dict, Callable, Tuple, Any

# Глобальний реєстр: Мапить (МЕТОД, ШЛЯХ) -> Функція
_routes: Dict[Tuple[str, str], Callable] = {}

def register_route(method: str, path: str) -> Callable:
    # Повертає декоратор, який реєструє функцію у глобальному словнику _routes.
    def decorator(func: Callable) -> Callable:
        _routes[(method, path)] = func
        return func
    return decorator

def get(path: str) -> Callable:
    """Декоратор для GET запитів."""
    return register_route("GET", path)

def post(path: str) -> Callable:
    """Декоратор для POST запитів."""
    return register_route("POST", path)

# Створення об'єкта app для доступу через крапку (напр., @app.get)
app = SimpleNamespace(get=get, post=post)