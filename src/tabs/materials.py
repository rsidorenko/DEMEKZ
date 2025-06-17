import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from database import DB_CONFIG

COLUMNS = (
    "Тип", "Наименование", "Поставщик", "Количество в упаковке", "Описание", "Стоимость", "Кол-во на складе", "Минимальное допустимое количество"
)

class MaterialsTab(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.conn = pymysql.connect(**DB_CONFIG)
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
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT m.id, mt.name as type_name, m.name, m.supplier_id, m.package_quantity, m.description, m.unit_price, m.stock_quantity, m.min_quantity
                FROM materials m
                JOIN material_types mt ON m.type = mt.id
            """)
            for row in cursor.fetchall():
                values = tuple("" if v is None else v for v in (
                    row['type_name'],
                    row['name'],
                    row['supplier_id'],
                    row['package_quantity'],
                    row['description'],
                    row['unit_price'],
                    row['stock_quantity'],
                    row['min_quantity']
                ))
                self.tree.insert("", tk.END, iid=str(row['id']), values=values)

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
                cursor.execute("DELETE FROM materials WHERE id=%s", (selected[0],))
            self.conn.commit()
            self.load_data()

    def open_form(self, initial=None, item_id=None):
        form = tk.Toplevel(self)
        form.title("Данные материала")
        form.geometry("400x600")
        form.resizable(False, False)
        form.grab_set()
        entries = {}
        # Получаем значения для дропдаунов
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT name, id FROM material_types")
            type_rows = cursor.fetchall()
            type_values = [row['name'] for row in type_rows]
            cursor.execute("SELECT name, id FROM suppliers")
            supplier_rows = cursor.fetchall()
            supplier_values = [row['name'] for row in supplier_rows]
            supplier_map = {row['name']: row['id'] for row in supplier_rows}
        def only_numeric(P):
            return P == "" or P.replace('.', '', 1).isdigit()
        vcmd = (form.register(only_numeric), '%P')
        for i, field in enumerate(COLUMNS):
            lbl = ttk.Label(form, text=field)
            lbl.pack(anchor="w", padx=10, pady=(10 if i == 0 else 5, 0))
            if field == "Тип":
                combo = ttk.Combobox(form, values=type_values, state="readonly")
                combo.pack(fill='x', padx=10, pady=2)
                if initial:
                    combo.set(initial[i])
                else:
                    combo.set(type_values[0] if type_values else "")
                entries[field] = combo
            elif field == "Поставщик":
                combo = ttk.Combobox(form, values=supplier_values, state="readonly")
                combo.pack(fill='x', padx=10, pady=2)
                if initial:
                    combo.set(initial[i])
                else:
                    combo.set(supplier_values[0] if supplier_values else "")
                entries[field] = combo
            elif field in ["Количество в упаковке", "Стоимость", "Кол-во на складе", "Минимальное допустимое количество"]:
                ent = ttk.Entry(form, validate='key', validatecommand=vcmd)
                ent.pack(fill='x', padx=10, pady=2)
                if initial:
                    ent.insert(0, initial[i])
                else:
                    if field == "Количество в упаковке":
                        ent.insert(0, "1")
                    else:
                        ent.insert(0, "0")
                entries[field] = ent
            else:
                ent = ttk.Entry(form)
                ent.pack(fill='x', padx=10, pady=2)
                if initial:
                    ent.insert(0, initial[i])
                else:
                    if field == "Наименование":
                        ent.insert(0, "Новый материал")
                    elif field == "Описание":
                        ent.insert(0, "")
                entries[field] = ent
        def save():
            data = [entries[f].get().strip() for f in COLUMNS]
            if not all(data):
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return
            supplier_name = entries["Поставщик"].get()
            supplier_id = supplier_map.get(supplier_name)
            if supplier_id is None:
                messagebox.showerror("Ошибка", f"Поставщик '{supplier_name}' не найден. Пожалуйста, выберите существующего поставщика.")
                return
            with self.conn.cursor() as cursor:
                if item_id:
                    cursor.execute("""
                        UPDATE materials SET type=(SELECT id FROM material_types WHERE name=%s), name=%s, supplier_id=%s, package_quantity=%s, description=%s, unit_price=%s, stock_quantity=%s, min_quantity=%s WHERE id=%s
                    """, (data[0], data[1], supplier_id, data[3], data[4], data[5], data[6], data[7], item_id))
                else:
                    cursor.execute("""
                        INSERT INTO materials (type, name, supplier_id, description, unit_price, stock_quantity, min_quantity, package_quantity, unit)
                        VALUES ((SELECT id FROM material_types WHERE name=%s), %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (data[0], data[1], supplier_id, data[4], data[5], data[6], data[7], data[3], 'шт'))
            self.conn.commit()
            form.destroy()
            self.load_data()
        ttk.Button(form, text="Сохранить", command=save).pack(pady=15) 