from typing import Optional, Tuple, Any, List
from .datatypes import DataType
from .row import Row

class Column:
    """Клас, що представляє стовпець таблиці."""

    def __init__(self, name: str, data_type: DataType, nullable: bool = True, 
                 unique: bool = False, references: Optional[Tuple[str, str]] = None):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.unique = unique
        self.references = references

    def __repr__(self) -> str:
        return f"<Column(name='{self.name}', type={self.data_type})>"

    def validate(self, value: Any) -> None:
        """Перевіряє тип та обмеження (nullable)."""
        if value is None:
            if not self.nullable:
                raise ValueError(f"Column '{self.name}' cannot be null.")
            return
        
        if not self.data_type.validate(value):
            raise TypeError(f"Invalid type for column '{self.name}'. Expected {self.data_type}.")

    def check_unique(self, value: Any, table_rows: List['Row']) -> None:
        """Перевіряє унікальність значення серед існуючих рядків."""
        if self.unique and value is not None:
            for row in table_rows:
                if row.get(self.name) == value:
                    raise ValueError(f"Unique constraint failed for column '{self.name}'.")

    def check_foreign_key(self, value: Any, database: Any) -> None:
        """Перевіряє зовнішній ключ."""
        if self.references and value is not None:
            ref_table_name, ref_col_name = self.references
            ref_table = database.get_table(ref_table_name)
            
            found = any(row[ref_col_name] == value for row in ref_table)
            if not found:
                raise ValueError(f"Foreign key constraint failed: {value} not found in {ref_table_name}.{ref_col_name}.")