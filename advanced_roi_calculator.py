"""
Улучшенный Калькулятор ROI (Return on Investment)
Поддерживает несколько инвестиций, хранение истории и графики доходности.
"""

import matplotlib.pyplot as plt
import csv
import sys # Импорт для более чистого выхода из программы

# Глобальная переменная для хранения истории
investment_history = []

def calculate_roi(investment, profit):
    """
    Рассчитывает процент ROI.
    ROI = ((Прибыль - Инвестиции) / Инвестиции) * 100
    """
    try:
        # Проверка на ноль перед делением
        if investment == 0:
            return None
            
        roi = (profit - investment) / investment * 100
        return roi
    except Exception as e:
        # Общая обработка ошибок, хотя ZeroDivisionError обрабатывается выше
        print(f"Произошла ошибка при расчете: {e}")
        return None

def show_summary():
    """
    Отображает сводную таблицу всех записанных инвестиций.
    """
    if not investment_history:
        print("История инвестиций пустая. Добавьте данные.")
        return
    
    # Расчет общей инвестиции и прибыли для сводной строки
    total_investment = sum(record['investment'] for record in investment_history)
    total_profit = sum(record['profit'] for record in investment_history)
    total_roi = calculate_roi(total_investment, total_profit)

    print("\n" + "="*50)
    print("Сводная таблица доходности:")
    print("="*50)
    # Форматирование для выравнивания
    print("{:<15} {:<15} {:<15} {:<5}".format("Инвестиции", "Доход", "ROI (%)", "ID"))
    print("-" * 50)

    for idx, record in enumerate(investment_history, 1):
        # Вывод данных для каждой отдельной инвестиции
        print("{:<15.2f} {:<15.2f} {:<15.2f} {:<5}".format(
            record['investment'], 
            record['profit'], 
            record['roi'], 
            idx
        ))
    
    print("-" * 50)
    # Вывод общей сводки
    print("{:<15.2f} {:<15.2f} {:<15.2f} {:<5}".format(
        total_investment, 
        total_profit, 
        total_roi if total_roi is not None else 0.0, 
        "ИТОГО"
    ))
    print("="*50)

def plot_graph():
    """
    Строит график ROI в зависимости от номера инвестиции.
    """
    if len(investment_history) < 1:
        print("Нет данных для графика. Добавьте как минимум одну инвестицию.")
        return

    ids = list(range(1, len(investment_history) + 1))
    rois = [record['roi'] for record in investment_history]

    plt.figure(figsize=(10, 6))
    plt.plot(ids, rois, marker='o', linestyle='-', color='green', label='ROI (%)')
    
    # Добавляем горизонтальную линию для нулевого ROI
    plt.axhline(0, color='r', linestyle='--', linewidth=0.8, label='Нулевой ROI')
    
    plt.title("Динамика ROI по инвестициям")
    plt.xlabel("Инвестиция №")
    plt.ylabel("ROI (%)")
    plt.xticks(ids) # Устанавливаем метки только для существующих инвестиций
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()

def save_to_csv(filename="roi_history.csv"):
    """
    Сохраняет историю инвестиций в CSV файл.
    """
    if not investment_history:
        print("Нет данных для сохранения.")
        return

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            # Убедимся, что все поля из словаря истории используются
            fieldnames = ['investment', 'profit', 'roi']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(investment_history)
        print(f"✅ История успешно сохранена в файл '{filename}'")
    except Exception as e:
        print(f"❌ Ошибка при сохранении в CSV: {e}")

def add_new_investment():
    """
    Запрашивает у пользователя данные для новой инвестиции и сохраняет их.
    """
    while True:
        try:
            print("\n--- Ввод новой инвестиции ---")
            investment = float(input("Введите сумму инвестиций: "))
            profit = float(input("Введите полученный доход (включая возврат инвестиций): "))
            
            roi = calculate_roi(investment, profit)
            if roi is None and investment == 0:
                print("❌ Инвестиции не могут быть нулевыми для расчета ROI.")
                continue # Начать ввод заново
            
            if roi is not None:
                print(f"✅ Доходность инвестиций (ROI): {roi:.2f}%")
                # Сохраняем только при успешном расчете
                investment_history.append({'investment': investment, 'profit': profit, 'roi': roi})
            
            break # Выход из цикла ввода после успешного добавления
            
        except ValueError:
            print("❌ Пожалуйста, введите корректное числовое значение.")
        except KeyboardInterrupt:
            # Обработка прерывания во время ввода
            print("\nВвод отменен.")
            break

def display_menu():
    """
    Отображает меню действий.
    """
    print("\n" + "="*30)
    print("МЕНЮ ДЕЙСТВИЙ:")
    print("1 - Добавить новую инвестицию")
    print("2 - Показать сводную таблицу")
    print("3 - Построить график ROI")
    print("4 - Сохранить историю в CSV")
    print("5 - Выход")
    print("="*30)

def main():
    """
    Основная функция программы с исправленной логикой цикла.
    """
    print("--- Добро пожаловать в Advanced ROI Calculator! ---")
    
    # Основной цикл управления, который постоянно показывает меню
    while True:
        display_menu()
        
        choice = input("Выберите действие (1-5): ").strip() # Удаляем пробелы
        
        if choice == '1':
            add_new_investment() # Вызываем отдельную функцию для ввода данных
        elif choice == '2':
            show_summary()
        elif choice == '3':
            plot_graph()
        elif choice == '4':
            save_to_csv()
        elif choice == '5':
            print("Спасибо за использование калькулятора! До свидания.")
            sys.exit(0) # Используем sys.exit для чистого завершения
        else:
            print(f"Неверный выбор '{choice}'. Пожалуйста, введите число от 1 до 5.")

if __name__ == "__main__":
    main()
