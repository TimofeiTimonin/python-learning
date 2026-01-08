import sqlite3
from datetime import datetime

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    trans_type TEXT,
                    category TEXT,
                    amount REAL)""")
def add_trans(trans_type, category, amount):
    cursor.execute("""INSERT INTO transactions(date, trans_type, category, amount)
                    VALUES (?, ?, ?, ?)""",(
                        datetime.now().strftime("%Y-%m-%d %H:%M"),
                        trans_type,
                        category,
                        amount
                        ))
    conn.commit()
    print("Транзакция добавлена и сохранена")

def show_history_transactions():
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    print("История операций")
    for row in rows:
        print(f"{row[0]}:{row[1]} | {row[2]}, {row[3]}, {row[4]}")
def show_balance():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE trans_type='расход'")
    total_expense = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE trans_type='доход'")
    total_income = cursor.fetchone()[0]
    print(f"""Ваш баланс: {total_income - total_expense} руб.
          Доходы: {total_income} руб.
          Расходы: {total_expense} руб.""")
while True:
    try:
        response = int(input(
            "Выберите команду:\n"
            "1 - добавить транзакцию\n"
            "2 - Показать историю транзакций\n"
            "3 - Показать баланс\n"
            "4 - удалить транзакцию\n"
            "5 - редактировать транзакцию\n"
            "6 - завершить работу\n"
        ))
    except ValueError:
        print("Введите число от 1 до 6!")
        continue

    if response == 1:
        try:
            trans_type = input("Введите тип транзакции (доход/расход): ").lower()
            if trans_type not in ('доход', 'расход'):
                print("Ошибка ввода: выберите тип транзакции из предложенных")
                continue
            category = input("Введите категорию транзакции (Еда, зарплата, транспорт и т. п.): ")
            amount = int(input("Введите сумму транзакции: "))
            if amount <= 0:
                print("Сумма не может быть отрицательной или равна нулю")
                continue
        except ValueError:
            print("Сумма должна быть числом")
            continue

        # Создаем транзакцию (дата будет автоматически установлена)
        add_trans(trans_type, category, amount)


    elif response == 2:
        show_history_transactions()

    elif response == 3:
        show_balance()

    elif response == 6:
        print("Рад был помочь)")
        break

    else:
        print("Выберите команду из предложенного списка и введите соответствующую цифру.")
