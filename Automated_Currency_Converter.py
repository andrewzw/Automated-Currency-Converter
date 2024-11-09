import requests
import os
from dotenv import load_dotenv
import customtkinter as ctk

load_dotenv()

# CONSTANTS
API_KEY = os.getenv("API_KEY")
BASE_URL = f"https://api.freecurrencyapi.com/v1/latest?apikey={os.getenv('API_KEY')}"
CURRENCIES = ["AUD", "MYR", "EUR", "USD", "CAD"]


# FUNCTIONS
def convert_currency(user_currency):
    currencies = ",".join(CURRENCIES)
    url = f"{BASE_URL}&base_currency={user_currency}&currencies={currencies}"

    try:
        response = requests.get(url)
        data = response.json()
        return data["data"]

    except Exception:
        print(f"\nInvalid currency, please try again.\nChoose from: {CURRENCIES}\n")
        return None


while True:
    user_currency = input(
        f"\nChoose from: {CURRENCIES}\nEnter the base currency: "
    ).upper()
    if user_currency == "Q":
        print("Exiting...")
        break

    data = convert_currency(user_currency)

    if not data:
        continue

    user_amount = float(input("Enter the amount: "))

    del data[f"{user_currency}"]
    for currency, value in data.items():
        print(f"{currency} : {value * user_amount}")

# GUI
import tkinter

tkinter._test()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.geometry("400x240")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="Currency Converter", font=("Arial", 24))
label.pack(pady=12, padx=10)

entry1 = ctk.CTkEntry(
    master=frame,
    placeholder_text=f"\nChoose from: {CURRENCIES}\nEnter the base currency: ",
)
entry1.pack(pady=12, padx=10)

entry2 = ctk.CTkEntry(master=frame, placeholder_text="Enter the amount")
entry2.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text="Convert", command=convert_currency)
button.pack(pady=12, padx=10)

root.mainloop()
