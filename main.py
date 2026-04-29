import matplotlib.pyplot as plt
from models import RegularExpense, ImportantExpense, LeisureExpense
from storage import ExpenseStorage
from utils import *

class ExpenseChartApp:
    """Главный класс приложения"""
    
    def __init__(self):
        self.storage = ExpenseStorage()
        self.expenses = self.storage.load()
        self.expense_types = {
            '1': ('Обычный', RegularExpense),
            '2': ('Важный', ImportantExpense),
            '3': ('Развлечение', LeisureExpense)
        }
    
    def run(self):
        """Запуск приложения"""
        while True:
            self._show_menu()
            choice = input("\nВыберите действие: ").strip()
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.delete_expense()
            elif choice == '4':
                self.filter_expenses()
            elif choice == '5':
                self.show_statistics()
            elif choice == '6':
                self.show_chart()
            elif choice == '7':
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    def _show_menu(self):
        """Отображение меню"""
        print("\n" + "="*50)
        print("💰 КОНСОЛЬНОЕ ПРИЛОЖЕНИЕ 'EXPENSE CHART'")
        print("="*50)
        print("1. Добавить расход")
        print("2. Просмотреть все расходы")
        print("3. Удалить расход")
        print("4. Фильтрация расходов")
        print("5. Статистика")
        print("6. Показать график расходов по категориям")
        print("7. Выход")
    
    def add_expense(self):
        """Добавление нового расхода"""
        print("\n--- Добавление расхода ---")
        
        # Выбор типа расхода
        print("Тип расхода:")
        for key, (name, _) in self.expense_types.items():
            print(f"{key}. {name}")
        
        type_choice = input("Выберите тип (1-3): ").strip()
        if type_choice not in self.expense_types:
            print("Неверный тип расхода")
            return
        
        _, expense_class = self.expense_types[type_choice]
        
        # Ввод суммы
        while True:
            try:
                amount_str = input("Сумма (₽): ")
                amount = validate_amount(amount_str)
                break
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        # Ввод категории
        while True:
            try:
                category = input("Категория (например: Еда, Транспорт): ")
                category = validate_category(category)
                break
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        # Ввод даты
        while True:
            try:
                date = input("Дата (ГГГГ-ММ-ДД, пусто - сегодня): ")
                if not date:
                    date = datetime.now().strftime("%Y-%m-%d")
                validate_date(date)
                break
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        # Создание и добавление расхода
        expense = expense_class(amount, category, date)
        self.expenses.append(expense)
        self.storage.save(self.expenses)
        print(f"✅ Расход успешно добавлен!")
    
    def view_expenses(self):
        """Просмотр всех расходов"""
        if not self.expenses:
            print("\n📭 Нет добавленных расходов")
            return
        
        print("\n--- Все расходы ---")
        print("Дата       | Категория       | Сумма (₽)")
        print("-" * 45)
        for i, expense in enumerate(self.expenses, 1):
            print(f"{i}. {expense}")
    
    def delete_expense(self):
        """Удаление расхода"""
        if not self.expenses:
            print("\n📭 Нет расходов для удаления")
            return
        
        self.view_expenses()
        try:
            index = int(input("\nВведите номер расхода для удаления: ")) - 1
            if 0 <= index < len(self.expenses):
                deleted = self.expenses.pop(index)
                self.storage.save(self.expenses)
                print(f"✅ Удален расход: {deleted}")
            else:
                print("Неверный номер")
        except ValueError:
            print("Введите корректное число")
    
    def filter_expenses(self):
        """Фильтрация расходов"""
        print("\n--- Фильтрация расходов ---")
        print("1. По категории")
        print("2. По периоду")
        print("3. По типу")
        
        choice = input("Выберите фильтр: ").strip()
        
        filtered = self.expenses.copy()
        
        if choice == '1':
            category = input("Введите категорию: ")
            filtered = filter_by_category(filtered, category)
        elif choice == '2':
            try:
                start = input("Начальная дата (ГГГГ-ММ-ДД): ")
                end = input("Конечная дата (ГГГГ-ММ-ДД): ")
                start_date = validate_date(start)
                end_date = validate_date(end)
                filtered = filter_by_period(filtered, start_date, end_date)
            except ValueError as e:
                print(f"Ошибка: {e}")
                return
        elif choice == '3':
            print("Типы: 1-Обычный, 2-Важный, 3-Развлечение")
            type_choice = input("Выберите тип: ")
            type_map = {'1': 'regular', '2': 'important', '3': 'leisure'}
            if type_choice in type_map:
                filtered = [e for e in filtered if e.get_type() == type_map[type_choice]]
        else:
            print("Неверный выбор")
            return
        
        if not filtered:
            print("\n📭 Расходы не найдены")
            return
        
        print(f"\n--- Найдено расходов: {len(filtered)} ---")
        total = calculate_total(filtered)
        for expense in filtered:
            print(expense)
        print(f"\n💰 ИТОГО: {total:.2f} ₽")
    
    def show_statistics(self):
        """Показ статистики"""
        if not self.expenses:
            print("\n📭 Нет данных для статистики")
            return
        
        total = calculate_total(self.expenses)
        print("\n📊 СТАТИСТИКА РАСХОДОВ")
        print("="*40)
        print(f"Всего расходов: {len(self.expenses)}")
        print(f"Общая сумма: {total:.2f} ₽")
        print(f"Средний расход: {total/len(self.expenses):.2f} ₽")
        
        # Статистика по категориям
        print("\nПо категориям:")
        summary = get_categories_summary(self.expenses)
        for category, amount in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100
            print(f"  {category:15}: {amount:8.2f} ₽ ({percentage:5.1f}%)")
    
    def show_chart(self):
        """Построение графика расходов"""
        if not self.expenses:
            print("\n📭 Нет данных для построения графика")
            return
        
        summary = get_categories_summary(self.expenses)
        
        if not summary:
            print("Нет данных для графика")
            return
        
        # Создание графика
        categories = list(summary.keys())
        amounts = list(summary.values())
        
        plt.figure(figsize=(10, 6))
        plt.bar(categories, amounts, color='skyblue', edgecolor='black')
        plt.xlabel('Категории расходов', fontsize=12)
        plt.ylabel('Сумма (₽)', fontsize=12)
        plt.title('Расходы по категориям', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        # Добавление значений на столбцы
        for i, (cat, val) in enumerate(zip(categories, amounts)):
            plt.text(i, val + max(amounts)*0.01, f'{val:.0f}₽', 
                    ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.show()

def main():
    """Точка входа в приложение"""
    app = ExpenseChartApp()
    app.run()

if __name__ == "__main__":
    main()

