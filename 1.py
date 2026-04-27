import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "books_data.json"


# Функция сохранения данных в JSON
def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Успех", "Данные сохранены в файл!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные:\n{e}")


# Функция загрузки данных из JSON
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                books.extend(data)
                update_book_list()
            if data:
                messagebox.showinfo("Успех", f"Загружено {len(data)} книг!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{e}")


# Функция добавления книги
def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = genre_var.get()
    pages = entry_pages.get().strip()

    # Проверка пустых полей
    if not title or not author or not pages:
        messagebox.showwarning("Внимание", "Все поля должны быть заполнены!")
        return

    # Проверка количества страниц на число
    if not pages.isdigit():
        messagebox.showwarning("Внимание", "Количество страниц должно быть числом!")
        return

    pages = int(pages)

    # Добавление книги в список
    book = {"title": title, "author": author, "genre": genre, "pages": pages}
    books.append(book)

    # Обновление списка на экране
    update_book_list()

    # Очистка полей
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_pages.delete(0, tk.END)
    combo_genre.current(0)

    messagebox.showinfo("Успех", f"Книга '{title}' добавлена!")


# Функция обновления списка
def update_book_list(book_list=None):
    book_listbox.delete(0, tk.END)
    if book_list is None:
        book_list = books
    for i, book in enumerate(book_list, 1):
        entry = f"{i}. '{book['title']}' - {book['author']}, {book['genre']}, {book['pages']} стр."
        book_listbox.insert(tk.END, entry)


# Функция фильтрации
def apply_filter():
    genre_filter = genre_filter_var.get()
    pages_filter = pages_filter_var.get()

    filtered_books = books[:]

    # Фильтр по жанру
    if genre_filter != "Все":
        filtered_books = [b for b in filtered_books if b['genre'] == genre_filter]

    # Фильтр по количеству страниц
    if pages_filter == ">200":
        filtered_books = [b for b in filtered_books if b['pages'] > 200]
    elif pages_filter == ">300":
        filtered_books = [b for b in filtered_books if b['pages'] > 300]
    elif pages_filter == ">500":
        filtered_books = [b for b in filtered_books if b['pages'] > 500]

    update_book_list(filtered_books)


# Функция сброса фильтров
def reset_filter():
    combo_genre_filter.current(0)
    combo_pages_filter.current(0)
    update_book_list()


# Функция удаления книги
def delete_book():
    selection = book_listbox.curselection()
    if not selection:
        messagebox.showwarning("Внимание", "Выберите книгу для удаления!")
        return

    index = selection[0]
    # Определяем, какой список используется (отфильтрованный или обычный)
    genre_filter = genre_filter_var.get()
    pages_filter = pages_filter_var.get()

    if genre_filter != "Все" or pages_filter != "Все":
        # При фильтрации нужно найти книгу в основном списке
        filtered_books = books[:]
        if genre_filter != "Все":
            filtered_books = [b for b in filtered_books if b['genre'] == genre_filter]
        if pages_filter == ">200":
            filtered_books = [b for b in filtered_books if b['pages'] > 200]
        elif pages_filter == ">300":
            filtered_books = [b for b in filtered_books if b['pages'] > 300]
        elif pages_filter == ">500":
            filtered_books = [b for b in filtered_books if b['pages'] > 500]

        book_to_delete = filtered_books[index]
        books.remove(book_to_delete)
    else:
        books.pop(index)

    update_book_list()
    messagebox.showinfo("Успех", "Книга удалена!")


# Функция очистки всех книг
def clear_all_books():
    if not books:
        messagebox.showinfo("Информация", "Список книг пуст!")
        return

    confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЕ книги?")
    if confirm:
        books.clear()
        update_book_list()
        messagebox.showinfo("Успех", "Все книги удалены!")


# Главное окно
root = tk.Tk()
root.title("Book Tracker - Трекер прочитанных книг")
root.geometry("800x600")

# Список книг
books = []

# Метка заголовка
title_label = tk.Label(root, text="Book Tracker", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Фрейм для формы ввода
input_frame = tk.LabelFrame(root, text="Добавить новую книгу", font=("Arial", 12))
input_frame.pack(pady=10, padx=20, fill="x")

# Поле: Название книги
tk.Label(input_frame, text="Название книги:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_title = tk.Entry(input_frame, width=40)
entry_title.grid(row=0, column=1, padx=10, pady=5)

# Поле: Автор
tk.Label(input_frame, text="Автор:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_author = tk.Entry(input_frame, width=40)
entry_author.grid(row=1, column=1, padx=10, pady=5)

# Поле: Жанр
tk.Label(input_frame, text="Жанр:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
genre_var = tk.StringVar()
genre_list = ["Роман", "Фантастика", "Детектив", "Научная литература", "Поэзия", "Биография", "Фэнтези", "Другое"]
combo_genre = ttk.Combobox(input_frame, textvariable=genre_var, values=genre_list, width=37, state="readonly")
combo_genre.grid(row=2, column=1, padx=10, pady=5)
combo_genre.current(0)

# Поле: Количество страниц
tk.Label(input_frame, text="Количество страниц:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_pages = tk.Entry(input_frame, width=40)
entry_pages.grid(row=3, column=1, padx=10, pady=5)

# Кнопка добавления книги
btn_add = tk.Button(input_frame, text="Добавить книгу", font=("Arial", 11), bg="#4CAF50", fg="white", command=add_book)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# Кнопки сохранения и загрузки
btn_frame = tk.Frame(input_frame)
btn_frame.grid(row=5, column=0, columnspan=2, pady=5)

btn_save = tk.Button(btn_frame, text="Сохранить в JSON", bg="#9C27B0", fg="white", command=save_data)
btn_save.pack(side=tk.LEFT, padx=5)

btn_load = tk.Button(btn_frame, text="Загрузить из JSON", bg="#9C27B0", fg="white", command=load_data)
btn_load.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(btn_frame, text="Удалить выбранную", bg="#F44336", fg="white", command=delete_book)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear_all = tk.Button(btn_frame, text="Очистить всё", bg="#FF5722", fg="white", command=clear_all_books)
btn_clear_all.pack(side=tk.LEFT, padx=5)

# Фрейм для фильтров
filter_frame = tk.LabelFrame(root, text="Фильтры", font=("Arial", 12))
filter_frame.pack(pady=10, padx=20, fill="x")

# Фильтр по жанру
tk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
genre_filter_var = tk.StringVar()
genre_filter_list = ["Все", "Роман", "Фантастика", "Детектив", "Научная литература", "Поэзия", "Биография", "Фэнтези",
                     "Другое"]
combo_genre_filter = ttk.Combobox(filter_frame, textvariable=genre_filter_var, values=genre_filter_list, width=25,
                                  state="readonly")
combo_genre_filter.grid(row=0, column=1, padx=10, pady=5)
combo_genre_filter.current(0)

# Фильтр по страницам
tk.Label(filter_frame, text="По страницам:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
pages_filter_var = tk.StringVar()
pages_filter_options = ["Все", ">200", ">300", ">500"]
combo_pages_filter = ttk.Combobox(filter_frame, textvariable=pages_filter_var, values=pages_filter_options, width=10,
                                  state="readonly")
combo_pages_filter.grid(row=0, column=3, padx=10, pady=5)
combo_pages_filter.current(0)

# Кнопки фильтров
btn_filter = tk.Button(filter_frame, text="Применить фильтр", bg="#2196F3", fg="white", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=5, pady=5)

btn_reset = tk.Button(filter_frame, text="Сбросить", bg="#FF9800", fg="white", command=reset_filter)
btn_reset.grid(row=0, column=5, padx=5, pady=5)

# Фрейм для списка книг
list_frame = tk.Frame(root)
list_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Список для отображения книг
book_listbox = tk.Listbox(list_frame, font=("Arial", 11), height=15)

# Полоса прокрутки
scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=book_listbox.yview)
book_listbox.configure(yscrollcommand=scrollbar.set)

book_listbox.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Запуск приложения
root.mainloop()