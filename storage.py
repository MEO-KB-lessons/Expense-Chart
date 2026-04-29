import json
import os
from datetime import datetime
from models import RegularExpense, ImportantExpense, LeisureExpense

class ExpenseStorage:
    """Класс для сохранения и загрузки данных"""
    
    def __init__(self, filename="data/expenses.json"):
        self.filename = filename
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Создание директории для данных"""
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def save(self, expenses):
        """Сохранение расходов в JSON"""
        data = [expense.to_dict() for expense in expenses]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """Загрузка расходов из JSON"""
        if not os.path.exists(self.filename):
            return []
        
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        expenses = []
        for item in data:
            expense_class = self._get_expense_class(item.get('type', 'regular'))
            expense = expense_class(
                amount=item['amount'],
                category=item['category'],
                date=item['date']
            )
            expenses.append(expense)
        
        return expenses
    
    def _get_expense_class(self, expense_type):
        """Получение класса расхода по типу"""
        classes = {
            'regular': RegularExpense,
            'important': ImportantExpense,
            'leisure': LeisureExpense
        }
        return classes.get(expense_type, RegularExpense)

