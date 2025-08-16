import os
import csv

FILE_NAME = 'expenses.csv'

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    with open(FILE_NAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])
    print("Expense added!") 

def view_expenses():
    if not os.path.exists(FILE_NAME):
        print("No expenses found!")
        return
    with open(FILE_NAME) as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"Dated: {row[0]}, Category: {row[1]}, Amount: {row[2]}")

def expense_summary():
    if not os.path.exists(FILE_NAME):
        print("No expense found!!")
        return
    expenses= {}
    with open(FILE_NAME, "r") as file:
        reader= csv.reader(file)
        for row in reader:
            category= row[1]
            amount = float(row[2])
            expenses[category]= expenses.get(category, 0) + amount
        print("Expense Summary:")
        for category, total in expenses.items():
            print(f"{category};{total}")

while True:
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View Expense")
    print("3. Expense Summary")
    print("4. Exit")

    choice= input("Choose an option")
    if choice=="1":
         add_expense()
    elif choice=="2":
        view_expenses()
    elif choice=="3":
        expense_summary()
    elif choice=="4":
        break
    else:
        print("Vadapav")
    

