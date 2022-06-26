import requests

from url_params import params, cookies, headers


class MvideoParser:
    GET_PRODUCTS_IDS_URL = 'https://www.mvideo.ru/bff/products/listing'
    GET_MODELS_INFO_URL = 'https://www.mvideo.ru/bff/product-details/list'
    GET_PRICES_URL = 'https://www.mvideo.ru/bff/products/prices'

    params = params
    cookies = cookies
    headers = headers

    def __init__(self):
        self.tv_info = {}

    def get_product_ids(self):
        response_with_product_ids = requests.get(self.GET_PRODUCTS_IDS_URL, params=params, cookies=cookies,
                                              headers=headers)
        products_ids = []
        if response_with_product_ids.status_code == 200:
            if total_product_number := response_with_product_ids.json()["body"].get('total'):
                products_ids.extend(response_with_product_ids.json()['body']['products'])
                while params['offset'] <= total_product_number:
                    params['offset'] += 24
                    response_with_product_ids = requests.get(self.GET_PRODUCTS_IDS_URL, params=params, cookies=cookies,
                                                             headers=headers)
                    products_ids.extend(response_with_product_ids.json()['body']['products'])
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

    def add_model_name_and_link_to_tv_info(self):
        json_data = self.get_json_data_and_params_from_products_ids()[0]
        response_with_models_info = requests.post(self.GET_MODELS_INFO_URL, cookies=cookies, headers=headers,
                                                             json=json_data)
        if response_with_models_info.status_code == 200:
            tv_models_info = response_with_models_info.json()['body']['products']
            for tv in tv_models_info:
                if product_id := tv.get('productId'):
                    self.tv_info[product_id] = {}
                if name := tv.get('name'):
                    self.tv_info[product_id]['name'] = name
                if name_translit := tv.get('nameTranslit'):
                    self.tv_info[product_id]['link'] = f'https://www.mvideo.ru/products/{name_translit}-{product_id}'
            return self.tv_info
        return None

    def add_prices_to_tv_info(self):
        params = self.get_json_data_and_params_from_products_ids()[1]
        response_with_prices_info = requests.get(self.GET_PRICES_URL, cookies=cookies, headers=headers, params=params)
        if response_with_prices_info.status_code == 200:
            for tv in response_with_prices_info.json()['body']['materialPrices']:
                if tv_prices_info := tv.get('price'):
                    tv_id = tv_prices_info.get('productId')
                    base_price = tv_prices_info.get('basePrice')
                    sales_price = tv_prices_info.get('salePrice')
                    if tv_id:
                        self.tv_info[tv_id]['base_price'], self.tv_info[tv_id]['sale_price'] = base_price, sales_price
            return self.tv_info
        return None

    def get_all_discounts_today(self):
        self.add_model_name_and_link_to_tv_info()
        self.add_prices_to_tv_info()
        tv_on_sale_links = set()
        for tv_id, tv_info in self.tv_info.items():
            if sale_price := tv_info.get('sale_price'):
                if tv_info['base_price'] > sale_price:
                    tv_on_sale_links.add(tv_info['link'])
        return tv_on_sale_links
