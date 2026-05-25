import json
from typing import Dict, List, Any
from .core.table import Table
from .core.column import Column

class Database:
    """Центральна точка доступу до бази даних."""

    def __init__(self, name: str):
        self.name = name
        self._tables: Dict[str, Table] = {}

    def create_table(self, name: str, columns: List[Column]) -> Table:
        """Створює нову таблицю."""
        if name in self._tables:
            raise ValueError(f"Table '{name}' already exists.")
        table = Table(name=name, columns=columns, database=self)
        self._tables[name] = table
        return table

    def get_table(self, name: str) -> Table:
        """Отримує таблицю за назвою."""
        if name not in self._tables:
            raise KeyError(f"Table '{name}' not found.")
        return self._tables[name]

    def save_to_json(self, filename: str) -> None:
        """Зберігає поточний стан бази даних у JSON-файл."""
        data = {name: table.to_dict() for name, table in self._tables.items()}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)