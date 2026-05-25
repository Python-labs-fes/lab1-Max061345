from typing import Any, Dict

class Condition:
    """Клас для обробки умов фільтрації (WHERE)."""
    
    def __init__(self, column: str, operator: str, value: Any):
        self.column = column
        self.operator = operator
        self.value = value

    def evaluate(self, row_data: Dict[str, Any]) -> bool:
        """Перевіряє, чи відповідає рядок заданій умові."""
        row_value = row_data.get(self.column)
        
        # Обробка випадку, коли значення None (щоб уникнути помилок порівняння)
        if row_value is None and self.operator != '=':
            return False

        if self.operator == '=':
            return row_value == self.value
        elif self.operator == '!=':
            return row_value != self.value
        elif self.operator == '>':
            return row_value > self.value
        elif self.operator == '<':
            return row_value < self.value
        elif self.operator == '>=':
            return row_value >= self.value
        elif self.operator == '<=':
            return row_value <= self.value
        elif self.operator == 'LIKE':
            return str(self.value) in str(row_value)
            
        raise ValueError(f"Unsupported operator: {self.operator}")