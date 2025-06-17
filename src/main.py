import tkinter as tk
from tkinter import ttk
import pymysql
from database import create_database, initialize_tables, DB_CONFIG
from dotenv import load_dotenv
from tabs.partners import PartnerTab
from tabs.materials import MaterialsTab
from tabs.products import ProductsTab
from tabs.suppliers import SuppliersTab
from tabs.employees import EmployeesTab
from style import style

load_dotenv()

# Подключение к базе данных


def connect_to_database():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("Успешное подключение к базе данных")
        return connection
    except pymysql.MySQLError as e:
        print(
            f"Ошибка подключения к базе данных: {e}")
        return None


def main():
    create_database()
    initialize_tables()
    db_connection = connect_to_database()

    root = tk.Tk()
    root.title("Образ плюс")
    root.geometry("1200x800")
    root.iconbitmap("./swagodem/src/assets/favicon.ico")

    style(root)

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    partners_tab = PartnerTab(notebook)
    notebook.add(partners_tab, text="Партнеры")

    materials_tab = MaterialsTab(notebook)
    notebook.add(materials_tab, text="Материалы")

    products_tab = ProductsTab(notebook)
    notebook.add(products_tab, text="Продукция")

    suppliers_tab = SuppliersTab(notebook)
    notebook.add(suppliers_tab, text="Поставщики")

    employees_tab = EmployeesTab(notebook)
    notebook.add(employees_tab, text="Сотрудники")

    root.mainloop()

    # Закрываем соединение с БД при выходе
    if db_connection:
        db_connection.close()
        print("Соединение с базой данных закрыто")


if __name__ == "__main__":
    main()
