from tkinter import ttk

BACKGROUND = "#ffffff"
SECONDARY_BG = "#BFD6F6"
ACCENT = "#405C73"
TEXT_COLOR = "#000000"


def style(root):

    root.configure(bg=BACKGROUND)

# Устанавливаем тему
    style = ttk.Style()
    style.theme_use("clam")


# Настраиваем стиль для всех кнопок (TButton)
    style.configure("TButton",
                    background=SECONDARY_BG,
                    foreground=TEXT_COLOR,
                    relief="flat")

# Меняем цвет фона и текста при наведении (active state)
    style.map("TButton",
              background=[("active", ACCENT)],
              foreground=[("active", BACKGROUND)])

# Настройка фона вкладок
    style.configure("TNotebook", background=BACKGROUND, borderwidth=0)
    style.configure("TNotebook.Tab", background=SECONDARY_BG,
                    foreground=TEXT_COLOR, padding=10)
    style.map("TNotebook.Tab",
              background=[("selected", ACCENT)],
              foreground=[("selected", "#ffffff")])

# Кнопки
    style.configure("Accent.TButton",
                    background=ACCENT,
                    foreground="#ffffff",
                    padding=6)
    style.map("Accent.TButton",
              background=[("active", SECONDARY_BG)])

# Treeview (таблица)
    style.configure("Treeview",
                    background=BACKGROUND,
                    foreground=TEXT_COLOR,
                    fieldbackground=BACKGROUND,
                    rowheight=30)
    style.map("Treeview",
              background=[("selected", SECONDARY_BG)],
              foreground=[("selected", ACCENT)])

# Настраиваем стиль для шапки таблицы
    style.configure("Treeview.Heading",
                    background=ACCENT,
                    foreground=BACKGROUND,
                    relief="flat")

    style.configure("TLabel",
                    background=SECONDARY_BG,
                    foreground=TEXT_COLOR,
                    relief="flat")
