import csv
from typing import List, Dict, Any, Iterator, Optional
from .column import Column
from .row import Row
from .datatypes import IntegerType, FloatType, BooleanType
from ..query.engine import SimpleQuery

class Table:
    """Координатор структури даних для таблиці."""

    def __init__(self, name: str, columns: List[Column], database: Any = None):
        self.name = name
        self.columns = {col.name: col for col in columns}
        self._rows: List[Row] = []
        self._auto_increment_id = 1
        self._database = database

    def __iter__(self) -> Iterator[Row]:
        return iter(self._rows)

    def __len__(self) -> int:
        return len(self._rows)

    def query(self) -> Any:
        """Створює об'єкт запиту для таблиці."""
        return SimpleQuery(self)

    def _validate_row_data(self, data: Dict[str, Any]) -> None:
        """Внутрішня перевірка даних перед вставкою/оновленням."""
        for col_name, column in self.columns.items():
            value = data.get(col_name)
            column.validate(value)
            column.check_unique(value, self._rows)
            if self._database:
                column.check_foreign_key(value, self._database)

    def insert(self, data: Dict[str, Any]) -> Row:
        """Вставляє новий рядок у таблицю (CREATE)."""
        row_id = data.get('id', self._auto_increment_id)
        data['id'] = row_id 
        
        self._validate_row_data(data)
        
        new_row = Row(id=row_id, data=data)
        self._rows.append(new_row)
        
        if row_id >= self._auto_increment_id:
            self._auto_increment_id = row_id + 1
            
        return new_row

    def get_row(self, conditions: Dict[str, Any]) -> Optional[Row]:
        """Отримує рядок за умовами (READ)."""
        for row in self._rows:
            if all(row.get(k) == v for k, v in conditions.items()):
                return row
        return None

    def update(self, row_id: int, new_data: Dict[str, Any]) -> Optional[Row]:
        """Оновлює існуючий рядок за його ID (UPDATE)."""
        for i, row in enumerate(self._rows):
            if row.id == row_id:
                # Готуємо словник з оновленими даними
                updated_data = row.to_dict()
                updated_data.update(new_data)
                updated_data['id'] = row_id  # Забороняємо змінювати ID
                
                # Тимчасово вилучаємо рядок, щоб check_unique не сварився на самого себе
                temp_row = self._rows.pop(i)
                try:
                    self._validate_row_data(updated_data)
                    new_row = Row(id=row_id, data=updated_data)
                    self._rows.insert(i, new_row)
                    return new_row
                except Exception as e:
                    # Відкат змін у разі помилки валідації
                    self._rows.insert(i, temp_row)
                    raise e
        return None

    def delete(self, row_id: int, cascade: bool = True) -> None:
        """Видаляє рядок за ID (DELETE). Підтримує каскадне видалення."""
        row_to_delete = next((row for row in self._rows if row.id == row_id), None)
        if not row_to_delete:
            return  # Рядок не знайдено

        # 1. Логіка каскадного видалення
        if cascade and self._database:
            # Проходимося по всіх таблицях у базі
            for table_name, table in self._database._tables.items():
                if table_name == self.name:
                    continue
                
                # Шукаємо колонки, які посилаються на поточну таблицю
                for col_name, column in table.columns.items():
                    if column.references and column.references[0] == self.name:
                        ref_col = column.references[1]  # Поле, на яке посилаються (напр. 'id')
                        deleted_value = row_to_delete.get(ref_col)
                        
                        if deleted_value is not None:
                            # Знаходимо всі залежні рядки
                            dependent_rows = [r for r in table._rows if r.get(col_name) == deleted_value]
                            # Рекурсивно видаляємо їх
                            for dep_row in dependent_rows:
                                table.delete(dep_row.id, cascade=True)

        # 2. Видалення самого рядка
        self._rows = [row for row in self._rows if row.id != row_id]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "auto_increment": self._auto_increment_id,
            "rows": [row.to_dict() for row in self._rows]
        }

    # ... (залиште методи export_to_csv та import_from_csv без змін)