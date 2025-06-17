import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from database import DB_CONFIG

COLUMNS = (
    "Артикул", "Тип", "Наименование", "Описание", "Стоимость", "Длина", "Ширина", "Высота", "Вес", "Время изготовления"
)

class ProductsTab(ttk.Frame):
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
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.article, pt.type_name, p.name, p.description, p.price, p.size_length, p.size_width, p.size_height, p.weight, p.manufacture_time
                FROM products p
                JOIN product_types pt ON p.type = pt.id
            """)
            for row in cursor.fetchall():
                values = tuple("" if v is None else v for v in (
                    row['article'],
                    row['type_name'],
                    row['name'],
                    row['description'],
                    row['price'],
                    row['size_length'],
                    row['size_width'],
                    row['size_height'],
                    row['weight'],
                    row['manufacture_time']
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
            messagebox.showwarning("Предупреждение", "Выберите продукцию для удаления")
            return
            
        # Проверяем, используется ли продукция в product_materials
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM product_materials 
            WHERE product_id = %s
        """, (selected[0],))
        result = cursor.fetchone()
        
        if result['count'] > 0:
            if not messagebox.askyesno(
                "Предупреждение", 
                "Эта продукция используется в составе материалов. Удаление может привести к ошибкам в данных. Продолжить?"
            ):
                return
                
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту продукцию?"):
            # Сначала удаляем все связи в product_materials
            cursor.execute("DELETE FROM product_materials WHERE product_id = %s", (selected[0],))
            # Затем удаляем саму продукцию
            cursor.execute("DELETE FROM products WHERE id = %s", (selected[0],))
            self.conn.commit()
            self.load_data()

    def open_form(self, initial=None, item_id=None):
        form = tk.Toplevel(self)
        form.title("Данные продукции")
        form.geometry("400x700")
        form.resizable(False, False)
        form.grab_set()
        entries = {}
        # Получаем значения для дропдауна типа
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT type_name FROM product_types")
            type_values = [row['type_name'] for row in cursor.fetchall()]
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
            elif field in ["Стоимость", "Длина", "Ширина", "Высота", "Вес"]:
                ent = ttk.Entry(form, validate='key', validatecommand=vcmd)
                ent.pack(fill='x', padx=10, pady=2)
                if initial:
                    ent.insert(0, initial[i])
                else:
                    ent.insert(0, "0")
                entries[field] = ent
            else:
                ent = ttk.Entry(form)
                ent.pack(fill='x', padx=10, pady=2)
                if initial:
                    ent.insert(0, initial[i])
                else:
                    if field == "Артикул":
                        ent.insert(0, "NEW-001")
                    elif field == "Наименование":
                        ent.insert(0, "Новая продукция")
                    elif field == "Описание":
                        ent.insert(0, "")
                    elif field == "Время изготовления":
                        ent.insert(0, "1 день")
                entries[field] = ent
        def save():
            data = [entries[f].get().strip() for f in COLUMNS]
            if not all(data):
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return
            with self.conn.cursor() as cursor:
                if item_id:
                    cursor.execute("""
                        UPDATE products SET article=%s, type=(SELECT id FROM product_types WHERE type_name=%s), name=%s, description=%s, price=%s, size_length=%s, size_width=%s, size_height=%s, weight=%s, manufacture_time=%s WHERE id=%s
                    """, (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], item_id))
                else:
                    cursor.execute("""
                        INSERT INTO products (article, type, name, description, price, size_length, size_width, size_height, weight, manufacture_time)
                        VALUES (%s, (SELECT id FROM product_types WHERE type_name=%s), %s, %s, %s, %s, %s, %s, %s, %s)
                    """, tuple(data))
            self.conn.commit()
            form.destroy()
            self.load_data()
        ttk.Button(form, text="Сохранить", command=save).pack(pady=15) 