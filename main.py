from tkinter import Tk, PhotoImage, ttk, Menu, IntVar, BooleanVar, Toplevel, messagebox, Text, END
import webbrowser
import secrets
import string


def block_input(event):
    if event.state & 0x0004 and event.keycode == 65:
        event.widget.event_generate("<<SelectAll>>")
        return
    if event.state & 0x0004 and event.keycode == 67:
        event.widget.event_generate("<<Copy>>")
        return
    return "break"


def custom_window(name, title, dev=False):
    if hasattr(root, name) and getattr(root, name) is not None:
        getattr(root, name).lift()
        getattr(root, name).focus()
        return

    window = Toplevel(root)
    window.title(title)
    window.resizable(width=False, height=False)
    window.focus()

    if dev:
        ttk.Label(window, image=image).pack(padx=10, pady=10)
    else:
        txt = Text(window, relief="solid", font=("TkDefaultFont"), wrap="word", width=83, height=26)
        with open("LICENSE.txt", "r", encoding="UTF-8") as f:
            content = f.read()
        txt.insert("1.0", content)
        txt.config(state="disabled")
        txt.bind("<Key>", block_input)
        txt.pack(padx=10, pady=10)

    def close_window():
        window.destroy()
        setattr(root, name, None)

    window.protocol("WM_DELETE_WINDOW", close_window)
    setattr(root, name, window)


def version():
    messagebox.showinfo(title="Версия", message="v5.3.0\n\n"
                                                "- Оптимизировано поле вывода пароля\n"
                                                "- Возвращена кнопка копирования\n"
                                                "- Упорядочено меню информации\n"
                                                "- Прочие косметические улучшения")


def developer(x2dfox=False, git=False):
    if x2dfox:
        custom_window(name="image_window", title="x2DFox", dev=True)
    elif git:
        choice = messagebox.askyesno(title="GitHub", message="Перейти на страницу разработчика?")
        if choice:
            webbrowser.open("https://github.com/x2DFox")
    else:
        choice = messagebox.askyesno(title="Telegram", message="Перейти в канал разработчика?")
        if choice:
            webbrowser.open("https://t.me/x2DFox")


def license():
    custom_window(name="license_window", title="BSD 3-Clause License")


def character():
    char = []
    if uppercase.get():
        char.extend(string.ascii_uppercase)
    if lowercase.get():
        char.extend(string.ascii_lowercase)
    if digit.get():
        char.extend(string.digits)
    if symbol.get():
        char.extend(string.punctuation)
    return char


def change(*args):
    label["text"] = f"Длина: {length.get()}"


def regulator(delta):
    current = length.get()
    nvalue = (current + delta)
    if 4 <= nvalue <= 64:
        length.set(nvalue)
        change()


def generate():
    char = character()
    if not char:
        messagebox.showerror(title="Ошибка", message="Не выбраны данные")
        return

    password = []
    for _ in range(length.get()):
        password.append(secrets.choice(char))
    entry.delete(0, END)
    entry.insert(0, ''.join(password))


def copy():
    if not entry.get():
        messagebox.showerror(title="Ошибка", message="Нечего копировать")
    else:
        root.clipboard_clear()
        root.clipboard_append(entry.get())


root = Tk()
root.title("Password Generator")
icon = PhotoImage(file="resources/16x16.png")
root.iconphoto(True, icon)
root.geometry("600x120")
root.resizable(width=False, height=False)

main_menu = Menu(tearoff=0)
file_menu = Menu(tearoff=0)
developer_menu = Menu(tearoff=0)

file_menu.add_command(label="Версия", command=version)
file_menu.add_cascade(label="Разработчик", menu=developer_menu)
file_menu.add_command(label="Лицензия", command=license)

developer_menu.add_command(label="x2DFox", command=lambda: developer(x2dfox=True))
image = PhotoImage(file="resources/developer.png")
developer_menu.add_command(label="GitHub", command=lambda: developer(git=True))
developer_menu.add_command(label="Telegram", command=lambda: developer())

main_menu.add_cascade(label="Информация", menu=file_menu)
root.config(menu=main_menu)

ttk.Frame(relief="solid").place(x=5, y=5, width=590, height=55)
uppercase = BooleanVar(value=True)
lowercase = BooleanVar(value=True)
digit = BooleanVar(value=True)
symbol = BooleanVar(value=True)
ttk.Checkbutton(text="[A-Z] Прописные", variable=uppercase).place(x=10, y=10, width=120)
ttk.Checkbutton(text="[a-z] Строчные", variable=lowercase).place(x=10, y=35, width=120)
ttk.Checkbutton(text="[0-9] Цифры", variable=digit).place(x=135, y=10, width=120)
ttk.Checkbutton(text="[#$%] Cимволы", variable=symbol).place(x=135, y=35, width=120)

length = IntVar(value=24)
label = ttk.Label(text=f"Длина: {length.get()}")
label.place(x=260, y=10, width=60)
ttk.Button(text="<", command=lambda: regulator(-1), width=1).place(x=260, y=30)
ttk.Scale(from_=4, to=64, orient="horizontal", variable=length, command=change, length=301).place(x=275, y=30)
ttk.Button(text=">", command=lambda: regulator(1), width=1).place(x=574, y=30)

entry = ttk.Entry()
entry.bind("<Key>", block_input)
entry.place(x=5, y=65, width=590)

ttk.Button(text="ГЕНЕРИРОВАТЬ", command=generate).place(x=5, y=90, width=293)
ttk.Button(text="КОПИРОВАТЬ", command=copy).place(x=302, y=90, width=293)

root.mainloop()
