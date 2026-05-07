# movie_library.py

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'movies_data.json'

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []

        self.create_input_fields()
        self.create_treeview()
        self.create_filters()
        self.load_data()

    def create_input_fields(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Название
        tk.Label(frame, text="Название:").grid(row=0, column=0)
        self.title_entry = tk.Entry(frame)
        self.title_entry.grid(row=0, column=1)

        # Жанр
        tk.Label(frame, text="Жанр:").grid(row=0, column=2)
        self.genre_entry = tk.Entry(frame)
        self.genre_entry.grid(row=0, column=3)

        # Год выпуска
        tk.Label(frame, text="Год выпуска:").grid(row=0, column=4)
        self.year_entry = tk.Entry(frame)
        self.year_entry.grid(row=0, column=5)

        # Рейтинг
        tk.Label(frame, text="Рейтинг (0-10):").grid(row=0, column=6)
        self.rating_entry = tk.Entry(frame)
        self.rating_entry.grid(row=0, column=7)

        # Кнопка добавления
        add_btn = tk.Button(frame, text="Добавить фильм", command=self.add_movie)
        add_btn.grid(row=0, column=8, padx=10)

    def create_treeview(self):
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading('title', text='Название')
        self.tree.heading('genre', text='Жанр')
        self.tree.heading('year', text='Год выпуска')
        self.tree.heading('rating', text='Рейтинг')
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        delete_btn = tk.Button(self.root, text="Удалить выбранное", command=self.delete_selected)
        delete_btn.pack(pady=5)

    def create_filters(self):
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0)
        self.filter_genre_var = tk.StringVar()
        self.filter_genre_entry = tk.Entry(filter_frame, textvariable=self.filter_genre_var)
        self.filter_genre_entry.grid(row=0, column=1)
        filter_genre_btn = tk.Button(filter_frame, text="Фильтр", command=self.filter_by_genre)
        filter_genre_btn.grid(row=0, column=2)

        tk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=3)
        self.filter_year_var = tk.StringVar()
        self.filter_year_entry = tk.Entry(filter_frame, textvariable=self.filter_year_var)
        self.filter_year_entry.grid(row=0, column=4)
        filter_year_btn = tk.Button(filter_frame, text="Фильтр", command=self.filter_by_year)
        filter_year_btn.grid(row=0, column=5)

        reset_btn = tk.Button(filter_frame, text="Сбросить фильтр", command=self.load_data)
        reset_btn.grid(row=0, column=6, padx=10)

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year_str = self.year_entry.get()
        rating_str = self.rating_entry.get()

        # Валидация
        if not year_str.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return
        year = int(year_str)

        if not self.is_valid_rating(rating_str):
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
            return
        rating = float(rating_str)

        record = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(record)
        self.save_data()
        self.load_data()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        values = self.tree.item(selected_item[0], 'values')
        self.movies = [m for m in self.movies if not (m['title'] == values[0] and m['genre'] == values[1] and str(m['year']) == values[2] and str(m['rating']) == values[3])]
        self.save_data()
        self.load_data()

    def is_valid_rating(self, rating_str):
        try:
            rating = float(rating_str)
            return 0 <= rating <= 10
        except ValueError:
            return False

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.movies = json.load(f)
        else:
            self.movies = []

        for item in self.tree.get_children():
            self.tree.delete(item)

        for m in self.movies:
            self.tree.insert('', tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def filter_by_genre(self):
        genre = self.filter_genre_var.get()
        filtered = [m for m in self.movies if m['genre'] == genre]
        self.display_filtered(filtered)

    def filter_by_year(self):
        year_str = self.filter_year_var.get()
        if not year_str.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return
        year = int(year_str)
        filtered = [m for m in self.movies if m['year'] == year]
        self.display_filtered(filtered)

    def display_filtered(self, filtered_movies):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for m in filtered_movies:
            self.tree.insert('', tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
# -------------------------------------------
# .gitignore
# -------------------------------------------
# Python cache and pyc files
__pycache__
# IDE folders
# Data file
movies_data.json
# -------------------------------------------
# README.md
# -------------------------------------------
#
# # Movie Library
#
# Автор: Ваша Фамилия Имя
#
# ## Описание
# Графическое приложение для хранения информации о фильмах. Позволяет добавлять фильмы, фильтровать по жанру и году, сохранять/загружать данные в JSON.
#
# ## Как запустить
# 1. Скопируйте файлы в папку.
# 2. Убедитесь, что установлен Python 3.
# 3. Запустите командой:
# ```bash
# python movie_library.py
# ```
#
# ## Использование
# - Введите название, жанр, год и рейтинг (от 0 до 10).
# - Нажмите «Добавить фильм».
# - Используйте фильтры по жанру и году и кнопку «Сбросить фильтр» для просмотра.
# - Для удаления выберите фильм и нажмите «Удалить выбранное».
#
# Данные сохраняются в файле `movies_data.json`.
