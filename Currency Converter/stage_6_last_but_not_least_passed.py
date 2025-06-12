import requests

# Dictionary cache for storing retrieved data
cache = {}


def retrieve_currency_rates(code_from: str, code_to: str = None) -> None:
    your_currency_code = code_from.lower()
    url = f"https://www.floatrates.com/daily/{your_currency_code}.json"

    # Request currency rate from daily web service
    resp = requests.get(url, timeout=5)  # Set timeout to avoid hanging indefinitely
    currency_json = resp.json()

    if code_to:
        cache[code_to.lower()] = currency_json.get(code_to.lower(), {}).get("rate", None)
    else:
        # Store exchange rates for USD and EUR only if they are NOT the base currency
        if your_currency_code != "usd":
            cache["usd"] = currency_json.get("usd", {}).get("rate", None)
        if your_currency_code != "eur":
            cache["eur"] = currency_json.get("eur", {}).get("rate", None)


def convert_to_currency(amount: float, rate: float) -> float:
    return amount * rate


def main():
    # First input, currency to exchange from.
    # print("Exchange from:")
    currency_code_from: str = input().lower()
    # Retrieve currency exchange rates data
    retrieve_currency_rates(currency_code_from)
    # print("Cache:", cache)

    ## Exchange loop
    # Second input, currency to exchange to.
    # Third input, amount to exchange.
    while True:
        # print("Exchange to:")
        currency_code_to: str = input().strip().lower()
        if currency_code_to == "":
            break

        # print("Amount:")
        amount_to_exchange = input().strip()
        if amount_to_exchange == "":
            break

        # Check if currency is already stored in cache
        print("Checking the cache...")
        if currency_code_to in cache:
            print("Oh! It is in the cache!")
            # print(cache)
            rate_to = cache[currency_code_to]
        else:
            print("Sorry, but it is not in the cache!")
            retrieve_currency_rates(currency_code_from, currency_code_to)
            rate_to = cache[currency_code_to]
            # print(cache)

        # Calculate and print result
        result = convert_to_currency(float(amount_to_exchange), rate_to)
        print(f"You received {result:.2f} {currency_code_to.upper()}.")


if __name__ == '__main__':
    main()