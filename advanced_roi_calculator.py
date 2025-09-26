"""
Advanced ROI Calculator
Поддерживает несколько инвестиций, хранение истории и графики доходности.
"""

import matplotlib.pyplot as plt
import csv

investment_history = []

def calculate_roi(investment, profit):
    try:
        roi = (profit - investment) / investment * 100
        return roi
    except ZeroDivisionError:
        print("Ошибка: инвестиции не могут быть нулевыми!")
        return None

def show_summary():
    if not investment_history:
        print("История инвестиций пустая.")
        return
    
    print("\nСводная таблица доходности:")
    print("{:<10} {:<10} {:<10} {:<10}".format("Инвестиции", "Доход", "ROI (%)", "ID"))
    for idx, record in enumerate(investment_history, 1):
        print("{:<10} {:<10} {:<10.2f} {:<10}".format(record['investment'], record['profit'], record['roi'], idx))

def plot_graph():
    if not investment_history:
        print("Нет данных для графика.")
        return

    ids = list(range(1, len(investment_history)+1))
    rois = [record['roi'] for record in investment_history]

    plt.plot(ids, rois, marker='o', linestyle='-', color='green')
    plt.title("ROI по инвестициям")
    plt.xlabel("Инвестиция №")
    plt.ylabel("ROI (%)")
    plt.grid(True)
    plt.show()

def save_to_csv(filename="roi_history.csv"):
    if not investment_history:
        print("Нет данных для сохранения.")
        return

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['investment', 'profit', 'roi'])
        writer.writeheader()
        writer.writerows(investment_history)
    print(f"История сохранена в {filename}")

def main():
    print("Добро пожаловать в Advanced ROI Calculator!")
    
    while True:
        try:
            investment = float(input("Введите сумму инвестиций: "))
            profit = float(input("Введите полученный доход: "))
        except ValueError:
            print("Пожалуйста, введите корректное число.")
            continue

        roi = calculate_roi(investment, profit)
        if roi is not None:
            print(f"Доходность инвестиций: {roi:.2f}%")
            investment_history.append({'investment': investment, 'profit': profit, 'roi': roi})

        print("\nВарианты действий:")
        print("1 - Добавить новую инвестицию")
        print("2 - Показать сводную таблицу")
        print("3 - Построить график ROI")
        print("4 - Сохранить историю в CSV")
        print("5 - Выход")
        
        choice = input("Выберите действие (1-5): ")
        if choice == '1':
            continue
        elif choice == '2':
            show_summary()
        elif choice == '3':
            plot_graph()
        elif choice == '4':
            save_to_csv()
        elif choice == '5':
            print("Спасибо за использование калькулятора!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
