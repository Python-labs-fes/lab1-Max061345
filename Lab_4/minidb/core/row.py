from typing import Dict, Any, Iterator

class Row:
    """Рядок таблиці, що зберігає дані."""

    def __init__(self, id: int, data: Dict[str, Any]):
        self.id = id
        self._data = data
        self._data['id'] = id 

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Row):
            return NotImplemented
        return self._data == other._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)
        
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)
        
    def to_dict(self) -> Dict[str, Any]:
        """Повертає словник даних рядка."""
        return self._data.copy()