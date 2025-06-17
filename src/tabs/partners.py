import tkinter as tk
from tkinter import ttk, messagebox
from utils import is_valid_email, is_valid_phone
from database import DB_CONFIG
from typing import Dict, Any
import pymysql

TYPES = ["Розничный магазин", "Оптовый магазин", "Интернет-магазин"]
COLUMNS = ("Тип", "Наименование", "ИНН", "Директор", "Телефон", "Email", "Рейтинг", "Объем продаж")

# Подключение к базе данных
conn = pymysql.connect(**DB_CONFIG)

class PartnerTab(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.tree = ttk.Treeview(self, columns=COLUMNS, show="headings")
        for col in COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Добавить", command=self.add_entry).pack(side=tk.LEFT, padx=50)
        ttk.Button(btn_frame, text="Редактировать", command=self.edit_entry).pack(side=tk.LEFT, padx=50)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_entry).pack(side=tk.LEFT, padx=50)

        self.load_data()


    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, type, name, inn, director, phone, email, rating, sales_volume FROM partners")
            for row in cursor.fetchall():
                values = tuple("" if v is None else v for k, v in row.items() if k != 'id')
                self.tree.insert("", tk.END, iid=row['id'], values=values)

    def add_entry(self):
        self.open_form()

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Выберите запись", "Выберите запись для редактирования")
            return
        current_values = self.tree.item(selected[0])["values"]
        self.open_form(current_values, selected[0])

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Выберите запись", "Выберите запись для удаления")
            return
        if messagebox.askyesno("Удалить", "Вы уверены, что хотите удалить запись?"):
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM partners WHERE id=%s", (selected[0],))
            conn.commit()
            self.load_data()

    def open_form(self, initial=None, item_id=None):
        form = tk.Toplevel(self)
        form.title("Данные партнёра")
        form.geometry("400x500")
        form.resizable(False, False)
        form.grab_set()

        entries = {}

        for i, field in enumerate(COLUMNS):
            lbl = ttk.Label(form, text=field)
            lbl.pack(anchor="w", padx=10, pady=(10 if i == 0 else 5, 0))

            if field == "Тип":
                combo = ttk.Combobox(form, values=TYPES, state="readonly")
                combo.pack(fill='x', padx=10, pady=2)
                if initial:
                    combo.set(initial[i])
                else:
                    combo.set(TYPES[0])
                entries[field] = combo
            else:
                ent = ttk.Entry(form)
                ent.pack(fill='x', padx=10, pady=2)
                if initial:
                    ent.insert(0, initial[i])
                else:
                    if field == "ИНН":
                        ent.insert(0, "000000000000")
                    elif field == "Телефон":
                        ent.insert(0, "+7-000-000-00-00")
                    elif field == "Email":
                        ent.insert(0, "test@example.com")
                    elif field == "Рейтинг":
                        ent.insert(0, "5")
                    elif field == "Объем продаж":
                        ent.insert(0, "0")
                    elif field == "Директор":
                        ent.insert(0, "Иванов И.И.")
                    elif field == "Наименование":
                        ent.insert(0, "Новый партнер")
                entries[field] = ent

        def save():
            data = [entries[f].get().strip() for f in COLUMNS]

            if not all(data):
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return

            try:
                rating = float(entries["Рейтинг"].get())
                if not (0 <= rating <= 5):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 5.")
                return

            if not is_valid_phone(entries["Телефон"].get()):
                messagebox.showerror("Ошибка", "Телефон должен быть в формате +7-XXX-XXX-XX-XX.")
                return

            if not is_valid_email(entries["Email"].get()):
                messagebox.showerror("Ошибка", "Введите корректный email.")
                return

            with conn.cursor() as cursor:
                if item_id:
                    cursor.execute("""
                        UPDATE partners SET type=%s, name=%s, inn=%s, director=%s, phone=%s,
                        email=%s, rating=%s, sales_volume=%s WHERE id=%s
                    """, (*data, item_id))
                else:
                    cursor.execute("""
                        INSERT INTO partners (type, name, inn, director, phone, email, rating, sales_volume)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, data)
            conn.commit()
            form.destroy()
            self.load_data()

        ttk.Button(form, text="Сохранить", command=save).pack(pady=15)
