from bs4 import BeautifulSoup
from decimal import Decimal
import requests


def convert(amount, cur_from, cur_to, date):
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'

    response = requests.get(url, params={'date_req': date})  # Использовать переданный requests
    soup = BeautifulSoup(response.content, 'xml')

    nominal = Decimal(soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string)
    value_to = Decimal(soup.find('CharCode', text=cur_to).find_next_sibling('Value').string.replace(',', '.'))

    if cur_from == 'RUR':
        rate = amount / (value_to / nominal)
    else:
        value_from = Decimal(soup.find('CharCode', text=cur_from).find_next_sibling('Value').string.replace(',', '.'))
        nominal_from = Decimal(soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string)

        rate = (value_from / nominal_from * amount) / (value_to / nominal)

    x = rate.quantize(Decimal('1000.1000'))
    return x




