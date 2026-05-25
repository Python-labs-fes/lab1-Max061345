import json
from typing import Any

def render_json(data: Any) -> str:
    return json.dumps(data)

def render_error(message: str) -> str:
    return json.dumps({"error": message})