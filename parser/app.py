import requests

from parser.url_params import params, cookies, headers


class MvideoParser:
    GET_PRODUCTS_IDS_URL = 'https://www.mvideo.ru/bff/products/listing'
    GET_MODELS_INFO_URL = 'https://www.mvideo.ru/bff/product-details/list'
    GET_PRICES_URL = 'https://www.mvideo.ru/bff/products/prices'

    params = params
    cookies = cookies
    headers = headers

    def get_product_ids(self):
        response_with_product_ids = requests.get(self.GET_PRODUCTS_IDS_URL, params=params, cookies=cookies, headers=headers)
        products_ids = response_with_product_ids.json()['body']['products']
        return products_ids

    def get_json_data_and_params_from_products_ids(self):
        products_ids = self.get_product_ids()
        json_data = {'productIds': products_ids}

        params = {
            'productIds': ', '.join(products_ids),
            'addBonusRubles': 'true',
            'isPromoApplied': 'true',
        }

        return json_data, params

    def get_response_with_models_info(self):
        json_data = self.get_json_data_and_params_from_products_ids()[0]
        response_with_models_info = response = requests.post(self.GET_MODELS_INFO_URL, cookies=cookies, headers=headers,
                                                             json=json_data)
        return response_with_models_info.text

    def get_response_with_prices_info(self):
        params = self.get_json_data_and_params_from_products_ids()[1]
        response_with_prices_info = requests.get(self.GET_PRICES_URL, cookies=cookies, headers=headers, params=params)
        return response_with_prices_info.text
