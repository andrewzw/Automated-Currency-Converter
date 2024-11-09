import requests
import os
from dotenv import load_dotenv

# CONSTANTS
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = f"https://api.freecurrencyapi.com/v1/latest?apikey={os.getenv('API_KEY')}"

CURRENCIES = ["AUD", "MYR", "EUR", "USD", "CAD"]


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
    user_currency = input("\nEnter the base currency: ").upper()
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
