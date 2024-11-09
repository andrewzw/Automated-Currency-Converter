import requests
import os
from dotenv import load_dotenv
import customtkinter as ctk

load_dotenv()

# CONSTANTS
API_KEY = os.getenv("API_KEY")
BASE_URL = f"https://api.freecurrencyapi.com/v1/latest?apikey={os.getenv('API_KEY')}"
CURRENCIES = ["AUD", "MYR", "EUR", "USD", "CAD"]

user_currency = ""


# FUNCTIONS
def convert_currency():
    try:
        amount = float(user_amount.get())
        currencies = ",".join(CURRENCIES)
        url = f"{BASE_URL}&base_currency={user_currency}&currencies={currencies}"
        response = requests.get(url)
        data = response.json()["data"]
        del data[f"{user_currency}"]

        # Create table-style result text
        result_text = "Conversion Results\n"
        result_text += "─" * 30 + "\n"  # Table header separator
        result_text += "Currency        Amount\n"
        result_text += "─" * 30 + "\n"  # Column header separator

        for currency, value in data.items():
            converted = value * amount
            # Format each row with fixed width
            result_text += f"{currency:<10} {converted:>10.2f}\n"

        result_text += "─" * 30  # Table bottom separator

        # Update the result label
        result_label.configure(
            text=result_text,
            font=("Courier", 14),  # Monospace font for better alignment
            justify="left",
        )

    except ValueError:
        result_label.configure(text="Please enter a valid number")
    except Exception as e:
        result_label.configure(text=f"Error: Invalid currency or conversion failed")


def currencyOption(currency):
    global user_currency
    user_currency = currency
    if user_currency:
        convert_currency()
    selected_currency_label.configure(text=f"Selected Currency: {currency}")


# Custom Tkinter GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.geometry("500x500")

# Frames
frame = ctk.CTkFrame(master=root)
# Create frames first and pack them immediately after the title label
button_frame1 = ctk.CTkFrame(master=frame, fg_color="transparent")
button_frame2 = ctk.CTkFrame(master=frame, fg_color="transparent")

# Create currency_buttons dynamically
# Currency button configuration
currencies_config = [
    {"currency": "AUD", "frame": button_frame1},
    {"currency": "MYR", "frame": button_frame1},
    {"currency": "EUR", "frame": button_frame1},
    {"currency": "USD", "frame": button_frame2},
    {"currency": "CAD", "frame": button_frame2},
]

currency_buttons = []
for config in currencies_config:
    button = ctk.CTkButton(
        master=config["frame"],
        text=config["currency"],
        command=lambda c=config["currency"]: currencyOption(c),
        width=80,
        height=25,
        fg_color=["#3B8ED0", "#1F6AA5"],
        hover_color=["#36719F", "#144870"],
    )
    currency_buttons.append(button)
    button.pack(side=ctk.LEFT, pady=5, padx=5)


# Create user_amount input
user_amount = ctk.CTkEntry(
    master=frame,
    placeholder_text="Enter the amount",
    width=200,
)

# Create StringVar to track entry changes
amount_var = ctk.StringVar()
user_amount.configure(textvariable=amount_var)


# Add trace to update results whenever the entry changes
def on_amount_change(*args):
    if user_currency:  # Only convert if a currency is selected
        convert_currency()


amount_var.trace_add("write", on_amount_change)

# Labels
label = ctk.CTkLabel(master=frame, text="Currency Converter", font=("Arial", 24))
currency_label = ctk.CTkLabel(master=frame, text=f"{user_currency}")
selected_currency_label = ctk.CTkLabel(
    master=frame, text="Selected Currency: None", font=("Arial", 16)
)
result_label = ctk.CTkLabel(
    master=frame, text=""
)  # Create a result label with empty text initially

# Pack
frame.pack(pady=20, padx=60, fill="both", expand=True)
label.pack(pady=12, padx=10)
button_frame1.pack(after=label, pady=2)
button_frame2.pack(pady=2)
user_amount.pack(pady=(20, 10))
selected_currency_label.pack(pady=(10, 5))
result_label.pack(pady=10)

root.mainloop()
