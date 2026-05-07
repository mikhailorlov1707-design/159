# quote_generator.py

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

DATA_FILE = 'quotes_history.json'

# Предопределённый список цитат
default_quotes = [
    {"text": "Будь собой; все остальные уже заняты.", "author": "Оскар Уайльд", "topic": "Саморазвитие"},
    {"text": "Жизнь — это 10% то, что с тобой происходит, и 90% — как ты реагируешь на это.", "author": "Чарльз Р. Свиндолл", "topic": "Мотивация"},
    {"text": "Лучше сделать и пожалеть, чем не сделать и пожалеть.", "author": "Неизвестный", "topic": "Мотивация"},
    {"text": "Образование — это самое мощное оружие, которое вы можете использовать, чтобы изменить мир.", "author": "Нельсон Мандела", "topic": "Образование"},
    {"text": "Только тот, кто рискует уйти далеко, может узнать, как далеко он может зайти.", "author": "Тони Роббинс", "topic": "Мотивация"},
]

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.quotes = default_quotes.copy()
        self.history = []

        self.load_data()

        self.create_widgets()

    def create_widgets(self):
        # Кнопка генерации
        self.generate_btn = tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote)
        self.generate_btn.pack(pady=10)

        # Отображение текущей цитаты
        self.quote_text = tk.Text(self.root, height=4, wrap='word')
        self.quote_text.pack(padx=10, pady=5)

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0)
        self.author_filter_var = tk.StringVar()
        self.author_filter_entry = tk.Entry(filter_frame, textvariable=self.author_filter_var)
        self.author_filter_entry.grid(row=0, column=1)
        btn_filter_author = tk.Button(filter_frame, text="Фильтр", command=self.filter_by_author)
        btn_filter_author.grid(row=0, column=2)

        tk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=3)
        self.topic_filter_var = tk.StringVar()
        self.topic_filter_entry = tk.Entry(filter_frame, textvariable=self.topic_filter_var)
        self.topic_filter_entry.grid(row=0, column=4)
        btn_filter_topic = tk.Button(filter_frame, text="Фильтр", command=self.filter_by_topic)
        btn_filter_topic.grid(row=0, column=5)

        reset_btn = tk.Button(filter_frame, text="Сбросить фильтры", command=self.load_data)
        reset_btn.grid(row=0, column=6, padx=10)

        # История
        tk.Label(self.root, text="История сгенерированных цитат:").pack()
        self.history_listbox = tk.Listbox(self.root, width=80, height=10)
        self.history_listbox.pack(padx=10, pady=5)

    def generate_quote(self):
        quote = random.choice(self.quotes)
        self.display_quote(quote)
        self.history.append(quote)
        self.update_history()

    def display_quote(self, quote):
        self.quote_text.delete('1.0', tk.END)
        display_text = f'"{quote["text"]}"\n— {quote["author"]} ({quote["topic"]})'
        self.quote_text.insert(tk.END, display_text)

    def update_history(self):
        self.save_data()
        self.refresh_history()

    def refresh_history(self):
        self.history_listbox.delete(0, tk.END)
        for q in self.history:
            self.history_listbox.insert(tk.END, f'"{q["text"]}" — {q["author"]} ({q["topic"]})')

    def filter_by_author(self):
        author = self.author_filter_var.get().strip()
        if not author:
            self.load_data()
            return
        filtered = [q for q in self.quotes if q["author"] == author]
        self.display_filtered(filtered)

    def filter_by_topic(self):
        topic = self.topic_filter_var.get().strip()
        if not topic:
            self.load_data()
            return
        filtered = [q for q in self.quotes if q["topic"] == topic]
        self.display_filtered(filtered)

    def display_filtered(self, filtered_quotes):
        self.quotes = filtered_quotes
        # Можно оставить текущую историю без фильтрации
        # или очистить текущие отображения цитат
        # В данном случае, чтобы не мешать генерации, ничего не делаем
        # Можно реализовать отдельное отображение, если нужно

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.history = data.get('history', [])
                self.quotes = data.get('quotes', default_quotes)
        else:
            self.history = []
            self.quotes = default_quotes.copy()
        self.refresh_history()

    def save_data(self):
        data = {
            'quotes': self.quotes,
            'history': self.history
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()

# -------------------------------------------
# .gitignore
# -------------------------------------------
# Python cache and pyc files
__pycach




# IDE folders



# Data file
quotes_history.json

# -------------------------------------------
# README.md
# -------------------------------------------
#
# # Random Quote Generator
#
# Автор: Ваша Фамилия Имя
#
# ## Описание
# Графическое приложение для генерации случайных цитат. Позволяет получать случайную цитату, фильтровать по автору и теме, а также сохранять историю генераций.
#
# ## Как запустить
# 1. Скопируйте файлы в папку.
# 2. Убедитесь, что установлен Python 3.
# 3. Запустите командой:
# ```bash
# python quote_generator.py
# ```
#
# ## Использование
# - Нажимайте «Сгенерировать цитату» для получения случайной цитаты.
# - Используйте фильтры по автору и теме для поиска.
# - Посмотрите историю сгенерированных цитат.
# - Все данные сохраняются в файле `quotes_history.json`.
