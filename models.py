from datetime import datetime
from abc import ABC, abstractmethod

class Expense(ABC):
    """Абстрактный базовый класс для расходов"""
    
    def __init__(self, amount: float, category: str, date: str):
        self._amount = amount
        self._category = category
        self._date = None
        self.set_date(date)
    
    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("Сумма должна быть положительной")
        self._amount = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Категория не может быть пустой")
        self._category = value
    
    @property
    def date(self):
        return self._date
    
    def set_date(self, date_str: str):
        """Установка даты с валидацией"""
        try:
            self._date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
    
    @abstractmethod
    def get_type(self):
        """Возвращает тип расхода"""
        pass
    
    def to_dict(self):
        """Конвертация в словарь для JSON"""
        return {
            'amount': self._amount,
            'category': self._category,
            'date': self._date.strftime("%Y-%m-%d"),
            'type': self.get_type()
        }
    
    def __str__(self):
        return f"{self._date.strftime('%Y-%m-%d')} | {self._category:15} | {self._amount:8.2f} ₽"

class RegularExpense(Expense):
    """Обычный расход"""
    
    def get_type(self):
        return "regular"

class ImportantExpense(Expense):
    """Важный расход (наследование)"""
    
    def get_type(self):
        return "important"
    
    def __str__(self):
        return f"[ВАЖНО] {super().__str__()}"

class LeisureExpense(Expense):
    """Расход на развлечения"""
    
    def get_type(self):
        return "leisure"

