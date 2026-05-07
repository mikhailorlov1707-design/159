# training_planner.py

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = 'training_data.json'

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = []

        self.create_input_fields()
        self.create_treeview()
        self.create_filters()
        self.load_data()

    def create_input_fields(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Дата
        tk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=1)

        # Тип тренировки
        tk.Label(frame, text="Тип тренировки:").grid(row=0, column=2)
        self.type_entry = tk.Entry(frame)
        self.type_entry.grid(row=0, column=3)

        # Длительность
        tk.Label(frame, text="Длительность (мин):").grid(row=0, column=4)
        self.duration_entry = tk.Entry(frame)
        self.duration_entry.grid(row=0, column=5)

        # Кнопка добавления
        add_btn = tk.Button(frame, text="Добавить тренировку", command=self.add_training)
        add_btn.grid(row=0, column=6, padx=10)

    def create_treeview(self):
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип тренировки')
        self.tree.heading('duration', text='Длительность (мин)')
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        delete_btn = tk.Button(self.root, text="Удалить выбранное", command=self.delete_selected)
        delete_btn.pack(pady=5)

    def create_filters(self):
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0)
        self.filter_type_var = tk.StringVar()
        self.filter_type_entry = tk.Entry(filter_frame, textvariable=self.filter_type_var)
        self.filter_type_entry.grid(row=0, column=1)
        filter_type_btn = tk.Button(filter_frame, text="Фильтр", command=self.filter_by_type)
        filter_type_btn.grid(row=0, column=2)

        tk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=3)
        self.filter_date_var = tk.StringVar()
        self.filter_date_entry = tk.Entry(filter_frame, textvariable=self.filter_date_var)
        self.filter_date_entry.grid(row=0, column=4)
        filter_date_btn = tk.Button(filter_frame, text="Фильтр", command=self.filter_by_date)
        filter_date_btn.grid(row=0, column=5)

        reset_btn = tk.Button(filter_frame, text="Сбросить фильтр", command=self.load_data)
        reset_btn.grid(row=0, column=6, padx=10)

    def add_training(self):
        date_str = self.date_entry.get()
        t_type = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Валидация
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты")
            return
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        record = {
            "date": date_str,
            "type": t_type,
            "duration": int(duration_str)
        }
        self.data.append(record)
        self.save_data()
        self.load_data()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        values = self.tree.item(selected_item[0], 'values')
        self.data = [d for d in self.data if not (d['date'] == values[0] and d['type'] == values[1] and str(d['duration']) == values[2])]
        self.save_data()
        self.load_data()

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = []

        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Отображение данных
        for record in self.data:
            self.tree.insert('', tk.END, values=(record['date'], record['type'], record['duration']))

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def filter_by_type(self):
        filter_type = self.filter_type_var.get()
        filtered = [d for d in self.data if d['type'] == filter_type]
        self.display_filtered(filtered)

    def filter_by_date(self):
        filter_date = self.filter_date_var.get()
        if not self.validate_date(filter_date):
            messagebox.showerror("Ошибка", "Некорректный формат даты")
            return
        filtered = [d for d in self.data if d['date'] == filter_date]
        self.display_filtered(filtered)

    def display_filtered(self, filtered_data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for record in filtered_data:
            self.tree.insert('', tk.END, values=(record['date'], record['type'], record['duration']))


if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
# ---------------------------
# .gitignore
# ---------------------------
# Python
__pycache__
# IDEs
# Data files
training_data.json
