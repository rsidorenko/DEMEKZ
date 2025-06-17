import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from database import DB_CONFIG
from tkcalendar import Calendar

COLUMNS = ("ФИО", "Дата рождения", "Паспортные данные", "Банковские реквизиты", "Наличие семьи", "Состояние здоровья")

class EmployeesTab(ttk.Frame):
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
            cursor.execute("SELECT id, full_name, birth_date, passport, bank_details, family, health FROM employees")
            for row in cursor.fetchall():
                values = tuple("" if v is None else v for v in (
                    row['full_name'], row['birth_date'], row['passport'], row['bank_details'], row['family'], row['health']
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
                # Удаляем самого сотрудника
                cursor.execute("DELETE FROM employees WHERE id=%s", (selected[0],))
            self.conn.commit()
            self.load_data()

    def open_form(self, initial=None, item_id=None):
        form = tk.Toplevel(self)
        form.title("Данные сотрудника")
        form.geometry("500x400")
        form.resizable(False, False)
        entries = {}
        defaults = {
            "ФИО": "Иванов Иван Иванович",
            "Дата рождения": "1990-01-01",
            "Паспортные данные": "0000 000000",
            "Банковские реквизиты": "00000000000000000000",
            "Наличие семьи": "Нет",
            "Состояние здоровья": "Хорошее"
        }
        for i, field in enumerate(COLUMNS):
            lbl = ttk.Label(form, text=field)
            lbl.pack(anchor="w", padx=10, pady=(10 if i == 0 else 5, 0))
            if field == "Дата рождения":
                frame = ttk.Frame(form)
                frame.pack(fill='x', padx=10, pady=2)
                ent = ttk.Entry(frame)
                ent.pack(side=tk.LEFT, fill='x', expand=True)
                if initial:
                    ent.insert(0, initial[i])
                else:
                    ent.insert(0, defaults[field])
                def open_calendar():
                    cal_win = tk.Toplevel(form)
                    cal_win.title("Выберите дату")
                    cal = Calendar(cal_win, selectmode='day', date_pattern='yyyy-mm-dd')
                    cal.pack(padx=10, pady=10)
                    def set_date():
                        ent.delete(0, tk.END)
                        ent.insert(0, cal.get_date())
                        cal_win.destroy()
                    ttk.Button(cal_win, text="Выбрать", command=set_date).pack(pady=5)
                btn = ttk.Button(frame, text="Календарь", command=open_calendar)
                btn.pack(side=tk.LEFT, padx=5)
                entries[field] = ent
            elif field == "Наличие семьи":
                var = tk.BooleanVar()
                if initial:
                    var.set(initial[i] == "Да")
                else:
                    var.set(defaults[field] == "Да")
                chk = ttk.Checkbutton(form, text="Есть семья", variable=var)
                chk.pack(anchor="w", padx=10, pady=2)
                entries[field] = var
            else:
                ent = ttk.Entry(form)
                ent.pack(fill='x', padx=10, pady=2)
                if initial:
                    ent.insert(0, initial[i])
                else:
                    ent.insert(0, defaults[field])
                entries[field] = ent
        def save():
            data = []
            for f in COLUMNS:
                if f == "Наличие семьи":
                    data.append("Да" if entries[f].get() else "Нет")
                elif f == "Дата рождения":
                    data.append(entries[f].get().strip())
                else:
                    data.append(entries[f].get().strip())
            if not all(data):
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return
            with self.conn.cursor() as cursor:
                if item_id:
                    cursor.execute("UPDATE employees SET full_name=%s, birth_date=%s, passport=%s, bank_details=%s, family=%s, health=%s WHERE id=%s", (*data, item_id))
                else:
                    cursor.execute("INSERT INTO employees (full_name, birth_date, passport, bank_details, family, health) VALUES (%s, %s, %s, %s, %s, %s)", tuple(data))
            self.conn.commit()
            form.destroy()
            self.load_data()
        ttk.Button(form, text="Сохранить", command=save).pack(pady=15) 