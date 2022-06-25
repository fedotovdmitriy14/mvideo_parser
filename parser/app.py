import requests

from parser.url_params import params, cookies, headers


class MvideoParser:
    GET_PRODUCTS_IDS_URL = 'https://www.mvideo.ru/bff/products/listing'
    GET_MODELS_INFO_URL = 'https://www.mvideo.ru/bff/product-details/list'
    GET_PRICES_URL = 'https://www.mvideo.ru/bff/products/prices'

    params = params
    cookies = cookies
    headers = headers

    def __init__(self):
        self._tv_info = {}

    def get_product_ids(self):
        response_with_product_ids = requests.get(self.GET_PRODUCTS_IDS_URL, params=params, cookies=cookies,
                                              headers=headers)
        products_ids = []
        if response_with_product_ids.status_code == 200:
            if total_product_number := response_with_product_ids.json()["body"].get('total'):
                while params['offset'] <= total_product_number:
                    products_ids.extend(response_with_product_ids.json()['body']['products'])
                    params['offset'] += 24
                    response_with_product_ids = requests.get(self.GET_PRODUCTS_IDS_URL, params=params, cookies=cookies,
                                                             headers=headers)
            params['offset'] = 0
            return products_ids
        return None

    def get_json_data_and_params_from_products_ids(self):
        if products_ids := self.get_product_ids():
            json_data = {'productIds': products_ids}
            params = {
                'productIds': ','.join(products_ids),
                'addBonusRubles': 'true',
                'isPromoApplied': 'true',
            }
            return json_data, params
        return None, None

    def add_model_info_to_tv_info(self):
        json_data = self.get_json_data_and_params_from_products_ids()[0]
        response_with_models_info = requests.post(self.GET_MODELS_INFO_URL, cookies=cookies, headers=headers,
                                                             json=json_data)
        if response_with_models_info.status_code == 200:
            tv_models_info = response_with_models_info.json()['body']['products']
            for tv in tv_models_info:
                if product_id := tv.get('productId'):
                    self._tv_info[product_id] = {}
                if name := tv.get('name'):
                    self._tv_info[product_id]['name'] = name
            return self._tv_info
        return None

    def add_prices_info_to_tv_info(self):
        params = self.get_json_data_and_params_from_products_ids()[1]
        response_with_prices_info = requests.get(self.GET_PRICES_URL, cookies=cookies, headers=headers, params=params)
        if response_with_prices_info.status_code == 200:
            for tv in response_with_prices_info.json()['body']['materialPrices']:
                if tv_prices_info := tv.get('price'):
                    tv_id = tv_prices_info.get('productId')
                    base_price = tv_prices_info.get('basePrice')
                    sales_price = tv_prices_info.get('salePrice')
                    if tv_id:
                        self._tv_info[tv_id]['base_price'], self._tv_info[tv_id]['sale_price'] = base_price, sales_price
            return self._tv_info
        return None


parser = MvideoParser()
# print(parser.get_product_ids())
print(parser.get_json_data_and_params_from_products_ids())
print(parser.add_model_info_to_tv_info())
print(parser.add_prices_info_to_tv_info())
