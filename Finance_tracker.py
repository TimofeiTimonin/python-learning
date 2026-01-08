import sqlite3
from datetime import datetime
#Создание базы данных
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    trans_type TEXT,
                    category TEXT,
                    amount REAL)""")
#добавление операции
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

#Показ истории
def show_history_transactions():
    cursor.execute("SELECT * FROM transactions ORDER BY date")
    rows = cursor.fetchall()
    print("История операций:")
    for i, row in enumerate(rows, 1):  # Начинаем с 1
        print(f"{i}. {row[1]} | {row[2]}, {row[3]}, {row[4]} руб. [ID: {row[0]}]")

#Баланс
def show_balance():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE trans_type='расход'")
    total_expense = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE trans_type='доход'")
    total_income = cursor.fetchone()[0]
    print(f"""Ваш баланс: {total_income - total_expense} руб.
          Доходы: {total_income} руб.
          Расходы: {total_expense} руб.""")

#Удаление операции
def delete_trans():
    show_history_transactions()  # теперь выводит с порядковыми номерами
    try:
        list_number = int(input("Введите номер транзакции для удаления: "))
        # Получаем ID в том же порядке, что и при выводе
        cursor.execute("SELECT id FROM transactions ORDER BY date")
        all_ids = cursor.fetchall()

        if 1 <= list_number <= len(all_ids):
            real_id = all_ids[list_number-1][0]  # Получаем реальный ID
            # Дальше удаляем по real_id
            cursor.execute("SELECT * FROM transactions WHERE id=?", (real_id,))
            if cursor.fetchone():
                confirm = input(f"Точно удалить транзакцию #{list_number}? (да/нет): ")
                if confirm.lower() != 'да':
                    print("Удаление отменено")
                    return
                cursor.execute("DELETE FROM transactions WHERE id=?", (real_id,))
                print("Транзакция удалена")
                conn.commit()
            else:
                print("Транзакция не найдена")
        else:
            print("Неверный номер транзакции")
    except ValueError:
        print("Введите корректный номер (число)")
#Редактирование операции
def edit_trans():
    show_history_transactions()
    try:
        trans_id = int(input("Введите ID транзакции для редактирования "))
        cursor.execute("SELECT * FROM transactions WHERE id=?", (trans_id,))
        trans = cursor.fetchone()
        if not trans:
            print("❌ Транзакция с таким ID не найдена")
            return

        print(f"Старая транзакция: Дата {trans[1]}, Тип {trans[2]}, Категория {trans[3]}, Сумма{trans[4]}")
        new_type = input("Введите новый тип транзакции (доход/расход, или нажмите Enter, чтобы оставить текущий): ").lower()
        new_category = input("Введите новую категорию транзакции (Еда, зарплата, транспорт и т. п., или нажмите Enter, чтобы оставить текущую): ")
        new_amount = input("Введите новую сумму транзакции( или нажмите Enter, чтобы оставить текущую): ")

        update_data = {
            'type': new_type if new_type in ('доход', 'расход') else trans[2],
            'category': new_category if new_category else trans[3],
            'amount': float(new_amount) if new_amount else trans[4]
        }

        # Выполняем обновление
        cursor.execute("""UPDATE transactions
                          SET trans_type=?, category=?, amount=?
                          WHERE id=?""",
                       (update_data['type'], update_data['category'], update_data['amount'], trans_id))
        conn.commit()
        print("✅ Транзакция обновлена")

    except ValueError:
        print("❌ Ошибка ввода данных")

#запуск программы
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

        add_trans(trans_type, category, amount)


    elif response == 2:
        show_history_transactions()

    elif response == 3:
        show_balance()

    elif response == 4:
        delete_trans()

    elif response == 5:
        edit_trans()

    elif response == 6:
        print("Рад был помочь)")
        break

    else:
        print("Выберите команду из предложенного списка и введите соответствующую цифру.")
