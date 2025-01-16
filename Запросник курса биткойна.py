
import requests  # Для выполнения HTTP-запросов
from tkinter import *  # Для создания графического интерфейса
from tkinter import ttk  # Для использования виджетов с улучшенным дизайном
from tkinter import messagebox as mb  # Для отображения сообщений
import json
import os
# Словарь кодов криптовалют и их полных названий
currencies = {
    "Bitcoin": "Биткойн",
    "Ethereum": "Эфириум",
    "Solana": "Солана",
    "Dash": "Dash",
    "Monero": "Монеро ",
    "Dogecoin": "Догекоин",
    "Litecoin": "Лайткоин ",
    "TRON": "ТРОН",
}

# Словарь кодов фиатных валют и их полных названий
currencies1 = {
    "USD": "Американский доллар",
    "EUR": "Евро",
    "JPY": "Японская йена",
    "GBP": "Британский фунт стерлингов",
    "CAD": "Канадский доллар",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "RUB": "Российский рубль",
}

def update_b_label(event):
    # Функция обновления метки с названием выбранной криптовалюты
    code = base_combobox.get()  # Получаем выбранный код
    name = currencies.get(code, "Неизвестная валюта")  # Получаем полное название
    b_label.config(text=name)  # Обновляем текст метки

def update_t_label(event):
    # Функция обновления метки с названием выбранной фиатной валюты
    code = target_combobox.get()  # Получаем выбранный код
    name = currencies1.get(code, "Неизвестная валюта")  # Получаем полное название
    t_label.config(text=name)  # Обновляем текст метки

def exchange():
    # Функция для получения курса обмена
    base_code = base_combobox.get()  # Получаем код исходной криптовалюты
    target_code = target_combobox.get()  # Получаем код целевой валюты

    if base_code and target_code:  # Проверяем, выбраны ли обе валюты
        try:
            # Выполняем запрос к API CoinGecko для получения курса
            response = requests.get(
                f'https://api.coingecko.com/api/v3/simple/price?ids={base_code.lower()}&vs_currencies={target_code.lower()}')
            response.raise_for_status()  # Проверяем, были ли ошибки в запросе

            data = response.json()  # Получаем данные в формате JSON

            # Извлекаем курс обмена
            exchange_rate = data.get(base_code.lower(), {}).get(target_code.lower(), None)

            if exchange_rate is not None:  # Проверяем, была ли найдена информация о курсе
                base = currencies[base_code]  # Получаем полное название криптовалюты
                target = currencies1[target_code]  # Получаем полное название фиатной валюты
                mb.showinfo("Курс обмена", f"Курс 1 {base} = {exchange_rate} {target}")  # Отображаем курс
            else:
                mb.showerror("Ошибка", f"Курс для валюты {target_code} не найден.")  # Сообщаем об ошибке
        except requests.exceptions.RequestException as e:  # Обработка исключений для запросов
            mb.showerror("Ошибка", f"Проблема с подключением: {e}")  # Сообщаем о проблеме с подключением
        except Exception as e:  # Обработка других ошибок
            mb.showerror("Ошибка", f"Ошибка: {e}")  # Сообщаем о другой ошибке
    else:
        mb.showwarning("Внимание", "Выберите коды валют.")  # Если валюты не выбраны, предупреждаем пользователя

def reset_selection():
    # Функция для сброса выбора
    base_combobox.set('')  # Сбрасываем выбор для криптовалюты
    target_combobox.set('')  # Сбрасываем выбор для фиатной валюты
    b_label.config(text='')  # Очищаем текст метки криптовалюты
    t_label.config(text='')  # Очищаем текст метки фиатной валюты

# Создание графического интерфейса
window = Tk()  # Инициализация главного окна
window.title("Курс крипто валют <<Меняла>>")  # Установка заголовка окна
window.geometry("400x360")  # Установка размера окна


Label(text="Криптовалюта:").pack(padx=10, pady=5)  # Создаем метку для выбора криптовалюты
base_combobox = ttk.Combobox(values=list(currencies.keys()), state="readonly")  # Создаем комбобокс для криптовалют
base_combobox.pack(padx=10, pady=5)  # Размещаем комбобокс в окне
base_combobox.bind("<<ComboboxSelected>>", update_b_label)  # Привязываем обновление метки к выбору

b_label = ttk.Label()  # Создаем метку для отображения названия выбранной криптовалюты
b_label.pack(padx=10, pady=10)  # Размещаем метку в окне

Label(text="Целевая (фиатная) валюта:").pack(padx=10, pady=5)  # Создаем метку для выбора целевой валюты
target_combobox = ttk.Combobox(values=list(currencies1.keys()), state="readonly")  # Создаем комбобокс для целевой валюты
target_combobox.pack(padx=5, pady=5)  # Размещаем комбобокс в окне
target_combobox.bind("<<ComboboxSelected>>", update_t_label)  # Привязываем обновление метки к выбору

t_label = ttk.Label()  # Создаем метку для отображения названия выбранной фиатной валюты
t_label.pack(padx=10, pady=5)  # Размещаем метку в окне

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)  # Кнопка для получения курса обмена
Button(text="Сбросить выбор", command=reset_selection).pack(padx=10, pady=10)  # Кнопка для сброса выбора

window.mainloop()  # Запуск главного цикла обработки событи

