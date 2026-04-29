from datetime import datetime, timedelta

def validate_amount(amount_str):
    """Проверка корректности суммы"""
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        return amount
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError("Введите корректное число")
        raise e

def validate_date(date_str):
    """Проверка корректности даты"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")

def validate_category(category):
    """Проверка категории"""
    if not category or not category.strip():
        raise ValueError("Категория не может быть пустой")
    return category.strip()

def filter_by_category(expenses, category):
    """Фильтрация расходов по категории"""
    return [e for e in expenses if e.category.lower() == category.lower()]

def filter_by_period(expenses, start_date, end_date):
    """Фильтрация расходов по периоду"""
    return [e for e in expenses if start_date <= e.date <= end_date]

def calculate_total(expenses):
    """Подсчёт суммы расходов"""
    return sum(e.amount for e in expenses)

def get_categories_summary(expenses):
    """Получение сводки по категориям для графика"""
    summary = {}
    for expense in expenses:
        summary[expense.category] = summary.get(expense.category, 0) + expense.amount
    return summary

