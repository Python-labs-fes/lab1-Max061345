# Файл: minidb_advanced/minidb/query/engine.py
from typing import List, Any, Dict, Optional
from .conditions import Condition

class SimpleQuery:
    """Клас для виконання запитів до таблиці з підтримкою Method Chaining та Агрегації."""

    def __init__(self, table: Any):
        self.table = table
        self._select_columns: Optional[List[str]] = None
        self._conditions: List[Condition] = []
        self._order_by_col: Optional[str] = None
        self._ascending: bool = True
        self._limit: Optional[int] = None
        self._offset: int = 0
        self._group_by_col: Optional[str] = None

    def select(self, columns: List[str]) -> 'SimpleQuery':
        self._select_columns = columns
        return self

    def where(self, column: str, operator: str, value: Any) -> 'SimpleQuery':
        self._conditions.append(Condition(column, operator, value))
        return self

    def order_by(self, column: str, ascending: bool = True) -> 'SimpleQuery':
        self._order_by_col = column
        self._ascending = ascending
        return self

    def limit(self, count: int) -> 'SimpleQuery':
        self._limit = count
        return self

    def offset(self, count: int) -> 'SimpleQuery':
        self._offset = count
        return self

    def execute(self) -> List[Dict[str, Any]]:
        """Виконує базовий складений запит та повертає результат."""
        results = []
        for row in self.table:
            row_dict = row.to_dict()
            if all(cond.evaluate(row_dict) for cond in self._conditions):
                results.append(row_dict)

        if self._order_by_col:
            results.sort(
                key=lambda x: (x.get(self._order_by_col) is None, x.get(self._order_by_col)), 
                reverse=not self._ascending
            )

        if self._offset:
            results = results[self._offset:]
        if self._limit is not None:
            results = results[:self._limit]

        if self._select_columns:
            filtered_results = []
            for row in results:
                filtered_results.append({col: row.get(col) for col in self._select_columns})
            return filtered_results

        return results

    def group_by(self, column: str) -> 'SimpleQuery':
        """Групує результати перед агрегацією."""
        self._group_by_col = column
        return self

    def count(self) -> Any:
        """Повертає кількість рядків (або словник з кількостями при group_by)."""
        results = self.execute()
        if self._group_by_col:
            grouped = {}
            for row in results:
                key = row.get(self._group_by_col)
                grouped[key] = grouped.get(key, 0) + 1
            return grouped
        return len(results)

    def sum(self, column: str) -> Any:
        """Повертає суму значень стовпця (або словник сум при group_by)."""
        results = self.execute()
        if self._group_by_col:
            grouped = {}
            for row in results:
                key = row.get(self._group_by_col)
                val = row.get(column)
                if isinstance(val, (int, float)):
                    grouped[key] = grouped.get(key, 0) + val
            return grouped
        return sum(row.get(column, 0) for row in results if isinstance(row.get(column), (int, float)))

    def avg(self, column: str) -> Any:
        """Повертає середнє значення стовпця (або словник середніх при group_by)."""
        results = self.execute()
        if self._group_by_col:
            grouped_sum = self.sum(column)
            grouped_count = self.count()
            return {k: (grouped_sum[k] / grouped_count[k] if grouped_count[k] > 0 else 0) 
                    for k in grouped_sum}
        
        valid_values = [row.get(column) for row in results if isinstance(row.get(column), (int, float))]
        if not valid_values:
            return 0.0
        return sum(valid_values) / len(valid_values)