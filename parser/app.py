import requests

from parser.url_params import params, cookies, headers

response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies, headers=headers)

print(response.json()['body']['products'])
