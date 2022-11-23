import json
import requests
from config import exchanges, payload, headers

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise APIException("Невозможно обработать одинаковые валюты")

        try:
            base_key = exchanges[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту <{base}>")

        try:
            quote_key = exchanges[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту <{quote}>")

        try:
            amount_key = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f"Не удалось обработать количество валюты <{amount}>")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_key}& \
        from={quote_key}&amount={amount_key}"
        response = requests.request("GET", url, headers=headers, data=payload)
        result_json = json.loads(response.content)

        return result_json['result']