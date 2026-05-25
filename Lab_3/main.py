from typing import Dict, Any
from framework import _routes
import views

def dispatch(request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method")
    path = request.get("path")
    
    handler_func = _routes.get((method, path))
    
    if handler_func:
        return handler_func(request)
    else:
        from templates import render_error
        return {
            "status_code": 404,
            "body": render_error("Not Found"),
            "headers": {"Content-Type": "application/json"}
        }