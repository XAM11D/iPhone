import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import requests
from io import BytesIO
import json

class PhoneShopApp:
    def __init__(self, master):
        self.master = master
        self.master.title("яблоки")
        self.data = None  # Данные о телефонах из файла JSON

        # Загрузка данных о телефонах из файла JSON
        with open("phones.json", "r", encoding="utf-8") as file:
            self.data = json.load(file)

        # Создание оболочки для прокрутки
        self.canvas = tk.Canvas(master, bg="#f0f0f0")
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.scrollable_frame.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel))
        self.scrollable_frame.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        # Настройка шрифта
        self.title_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=10)

        # Отображение всех телефонов
        row_counter = 0
        col_counter = 0
        for phone in self.data["phones"]:
            title = phone["Назва"]
            img_url = phone["Зоображення"]

            # Создание рамки для каждого телефона
            phone_frame = tk.Frame(self.scrollable_frame, relief="solid", bd=1, bg="white", padx=10, pady=10)
            phone_frame.grid(row=row_counter, column=col_counter, padx=20, pady=20, sticky="nsew")

            # Добавление информации о телефоне
            label_title = tk.Label(phone_frame, text=title, font=self.title_font, bg="white")
            label_title.pack(pady=10)

            # Загрузка изображения из URL и изменение размера без искажений
            response = requests.get(img_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((200, 200))  # Уменьшаем изображение, сохраняя пропорции
            photo = ImageTk.PhotoImage(img)

            label_img = tk.Label(phone_frame, image=photo, bg="white")
            label_img.photo = photo  # Сохранение ссылки на изображение
            label_img.pack(pady=10)

            # Создание кнопки "Посмотреть подробности"
            details_button = tk.Button(phone_frame, text="Подивитись характеристики", font=self.button_font,
                                       command=lambda p=phone: self.show_details(p), bg="#0078D7", fg="white")
            details_button.pack(pady=20)

            # Обновление счетчиков для следующего телефона
            col_counter += 1
            if col_counter == 3:  # Количество столбцов изменено на 3
                row_counter += 1
                col_counter = 0

        # Растягиваем рамки внутри оболочки
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(row_counter, weight=1)

    def show_details(self, phone):
        details_window = tk.Toplevel(self.master)
        details_window.title("Характеристики")
        details_window.configure(bg="#f0f0f0")

        # Создание и расположение меток и полей для отображения и редактирования характеристик телефона
        entry_vars = {}  # Словарь для хранения переменных ввода
        for i, (key, value) in enumerate(phone.items()):
            if key != "Зоображення":  # Пропустить изображение
                label_key = tk.Label(details_window, text=key, bg="#f0f0f0", font=self.title_font)
                label_key.grid(row=i, column=0, sticky="e", padx=10, pady=5)

                entry_var = tk.StringVar(value=value)
                entry = tk.Entry(details_window, textvariable=entry_var, width=70)
                entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
                entry_vars[key] = entry_var  # Сохранение переменной ввода в словаре

        # Создание кнопки "Сохранить"
        save_button = tk.Button(details_window, text="Зберегти", font=self.button_font, bg="#0078D7", fg="white",
                                command=lambda: self.save_details(phone, entry_vars))
        save_button.grid(row=len(phone), columnspan=2, pady=10, sticky="ew", padx=10)

        # Установка минимального размера окна
        details_window.update_idletasks()
        details_window.minsize(details_window.winfo_reqwidth(), details_window.winfo_reqheight())

    def save_details(self, phone, entry_vars):
        # Обновление данных телефона на основе введенных пользователем значений
        for key, value in entry_vars.items():
            phone[key] = value.get()

        # Сохранение обновленных данных в файле JSON
        with open("phones.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")


def main():
    root = tk.Tk()
    app = PhoneShopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
