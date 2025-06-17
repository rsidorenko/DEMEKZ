import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from database import DB_CONFIG

COLUMNS = ("Тип", "Наименование", "ИНН")
TYPES = ["Розничный магазин", "Оптовый магазин", "Интернет-магазин"]

class SuppliersTab(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.conn = pymysql.connect(**DB_CONFIG)
        self.tree = ttk.Treeview(self, columns=COLUMNS, show="headings")
        for col in COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Добавить", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Редактировать", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_entry).pack(side=tk.LEFT, padx=5)

        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id, supplier_type, name, inn FROM suppliers")
            for row in cursor.fetchall():
                values = tuple("" if v is None else v for v in (
                    row['supplier_type'], row['name'], row['inn']
                ))
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
            with self.conn.cursor() as cursor:
                # Удаляем все материалы, связанные с этим поставщиком
                cursor.execute("DELETE FROM materials WHERE supplier_id=%s", (selected[0],))
                # Удаляем самого поставщика
                cursor.execute("DELETE FROM suppliers WHERE id=%s", (selected[0],))
            self.conn.commit()
            self.load_data()

    def open_form(self, initial=None, item_id=None):
        form = tk.Toplevel(self)
        form.title("Данные поставщика")
        form.geometry("400x300")
        form.resizable(False, False)
        form.grab_set()
        entries = {}
        fields = ["Тип", "Наименование", "ИНН"]
        def only_numeric(P):
            return P == "" or P.isdigit()
        vcmd = (form.register(only_numeric), '%P')
        for i, field in enumerate(fields):
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
            elif field == "ИНН":
                ent = ttk.Entry(form, validate='key', validatecommand=vcmd)
                ent.pack(fill='x', padx=10, pady=2)
                if initial:
                    ent.insert(0, initial[i])
                else:
                    ent.insert(0, "000000000000")
                entries[field] = ent
            else:
                ent = ttk.Entry(form)
                ent.pack(fill='x', padx=10, pady=2)
                if initial:
                    ent.insert(0, initial[i])
                else:
                    ent.insert(0, "Новый поставщик")
                entries[field] = ent
        def save():
            data = [entries[f].get().strip() for f in fields]
            if not all(data):
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return
            with self.conn.cursor() as cursor:
                if item_id:
                    cursor.execute("UPDATE suppliers SET supplier_type=%s, name=%s, inn=%s WHERE id=%s", (*data, item_id))
                else:
                    cursor.execute("INSERT INTO suppliers (supplier_type, name, inn) VALUES (%s, %s, %s)", tuple(data))
            self.conn.commit()
            form.destroy()
            self.load_data()
        ttk.Button(form, text="Сохранить", command=save).pack(pady=15) 