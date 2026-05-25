from typing import Any

class DataType:
    """Базовий клас для типів даних бази."""
    
    def validate(self, value: Any) -> bool:
        """Перевіряє, чи відповідає значення типу даних."""
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__

    @classmethod
    def from_string(cls, name: str) -> 'DataType':
        """Створює екземпляр типу на основі рядкового опису."""
        types = {
            "INTEGER": IntegerType,
            "STRING": StringType,
            "BOOLEAN": BooleanType,
            "FLOAT": FloatType
        }
        name_upper = name.upper()
        if name_upper in types:
            return types[name_upper]()
        raise ValueError(f"Unknown data type: {name}")

class IntegerType(DataType):
    def validate(self, value: Any) -> bool:
        return isinstance(value, int)

class StringType(DataType):
    def validate(self, value: Any) -> bool:
        return isinstance(value, str)

class BooleanType(DataType):
    def validate(self, value: Any) -> bool:
        return isinstance(value, bool)

class FloatType(DataType):
    def validate(self, value: Any) -> bool:
        return isinstance(value, float)