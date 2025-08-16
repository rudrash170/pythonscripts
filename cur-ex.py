import os
import requests

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')

def check_exchange_rate(base_currency, target_currencies, amount):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    print(f"Request URL: {url}")  # Debugging: Print the URL
    
    try:
        response = requests.get(url)
        print(f"Response Status Code: {response.status_code}")  # Debugging: Print status code
        print(f"Response Content: {response.content.decode('utf-8')}")  # Debugging: Print response content
        
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        
        if 'conversion_rates' not in data:
            print("Error: 'conversion_rates' not found in the response.")
            return
        
        for currency in target_currencies:
            rate = data['conversion_rates'].get(currency)
            if rate:
                converted_amount = amount * rate
                print(f"{amount} {base_currency} = {converted_amount:.2f} {currency}")
            else:
                print(f"Exchange rate for {currency} not found.")
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP request failed: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")

# Get user input
base_currency = input("Enter the base currency (e.g., INR): ").upper()
target_currencies = input("Enter the target currencies separated by commas (e.g., USD,EUR,JPY): ").upper().split(',')
amount = float(input("Enter the amount to be converted: "))

check_exchange_rate(base_currency, target_currencies, amount)