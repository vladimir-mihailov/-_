import requests  # Для выполнения HTTP-запросов
from tkinter import *  # Для создания графического интерфейса
from tkinter import ttk  # Для использования виджетов с улучшенным дизайном
from tkinter import messagebox as mb  # Для отображения сообщений
import os  # Для проверки наличия файлов

# Словарь кодов криптовалют и их полных названий
currencies = {
    "Bitcoin": "Биткойн",
    "Ethereum": "Эфириум",
    "Solana": "Солана",
    "Dash": "Dash",
    "Monero": "Монеро",
    "Dogecoin": "Догекоин",
    "Litecoin": "Лайткоин",
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
    """Обновление метки с названием выбранной криптовалюты"""
    code = base_combobox.get()
    name = currencies.get(code, "Неизвестная валюта")
    b_label.config(text=name)

def update_t_label(event):
    """Обновление метки с названием выбранной фиатной валюты"""
    code = target_combobox.get()
    name = currencies1.get(code, "Неизвестная валюта")
    t_label.config(text=name)

def exchange():
    """Получение курса обмена через API CoinGecko"""
    base_code = base_combobox.get()
    target_code = target_combobox.get()

    if base_code and target_code:
        try:
            # Выполняем запрос к API CoinGecko
            response = requests.get(
                f'https://api.coingecko.com/api/v3/simple/price?ids={base_code.lower()}&vs_currencies={target_code.lower()}'
            )
            response.raise_for_status()  # Проверяем, была ли ошибка в запросе

            data = response.json()
            exchange_rate = data.get(base_code.lower(), {}).get(target_code.lower(), None)

            if exchange_rate is not None:
                base = currencies[base_code]
                target = currencies1[target_code]
                mb.showinfo("Курс обмена", f"Курс 1 {base} = {exchange_rate} {target}")
            else:
                mb.showerror("Ошибка", f"Курс для валюты {target_code} не найден.")
        except requests.exceptions.RequestException as e:
            mb.showerror("Ошибка", f"Проблема с подключением: {e}")
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning("Внимание", "Выберите коды валют.")

def reset_selection():
    """Сброс выбора валют"""
    base_combobox.set('')
    target_combobox.set('')
    b_label.config(text='')
    t_label.config(text='')

# Создание графического интерфейса
window = Tk()
window.title("Курс криптовалют <<Меняла>>")
window.geometry("400x360")

# Проверка наличия иконки
if os.path.exists("i.ico"):
    window.iconbitmap(default="i.ico")

Label(text="Криптовалюта:").pack(padx=10, pady=5)
base_combobox = ttk.Combobox(values=list(currencies.keys()), state="readonly")
base_combobox.pack(padx=10, pady=5)
base_combobox.bind("<<ComboboxSelected>>", update_b_label)

b_label = ttk.Label()
b_label.pack(padx=10, pady=10)

Label(text="Целевая (фиатная) валюта:").pack(padx=10, pady=5)
target_combobox = ttk.Combobox(values=list(currencies1.keys()), state="readonly")
target_combobox.pack(padx=5, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=5)

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)
Button(text="Сбросить выбор", command=reset_selection).pack(padx=10, pady=10)

window.mainloop()