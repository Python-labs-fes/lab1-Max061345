from typing import List, Iterator, Any
from .table import Table
from .row import Row

class JoinedTable:
    """Клас, що представляє внутрішнє з'єднання (INNER JOIN) двох таблиць."""

    def __init__(self, table1: Table, table2: Table, join_col1: str, join_col2: str):
        self.table1 = table1
        self.table2 = table2
        self.join_col1 = join_col1
        self.join_col2 = join_col2
        
        self._rows: List[Row] = self._perform_inner_join()

    def _perform_inner_join(self) -> List[Row]:
        """Реалізує логіку INNER JOIN з префіксами стовпців."""
        joined_rows = []
        new_row_id = 1

        for row1 in self.table1:
            for row2 in self.table2:
                val1 = row1.get(self.join_col1)
                val2 = row2.get(self.join_col2)

                if val1 == val2 and val1 is not None:
                    merged_data = {}
                    
                    for key, value in row1._data.items():
                        merged_data[f"{self.table1.name}.{key}"] = value
                        
                    for key, value in row2._data.items():
                        merged_data[f"{self.table2.name}.{key}"] = value

                    new_row = Row(id=new_row_id, data=merged_data)
                    joined_rows.append(new_row)
                    new_row_id += 1

        return joined_rows

    def __iter__(self) -> Iterator[Row]:
        """Дозволяє перебирати результати з'єднання у циклі."""
        return iter(self._rows)

    def __len__(self) -> int:
        """Повертає кількість знайдених збігів."""
        return len(self._rows)