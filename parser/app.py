import requests

from parser.url_params import params, cookies, headers


def get_product_ids(url='https://www.mvideo.ru/bff/products/listing'):
    response_with_product_ids = requests.get(url, params=params,
                                             cookies=cookies, headers=headers)
    products_ids = response_with_product_ids.json()['body']['products']
    return products_ids


def get_json_data_and_params_from_products_ids(products_ids):
    json_data = {'productIds': products_ids}

    params = {
        'productIds': ', '.join(products_ids),
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
    }

    return json_data, params


def get_response_with_models_info(json_data, url='https://www.mvideo.ru/bff/product-details/list'):
    response_with_models_info = response = requests.post(url, cookies=cookies, headers=headers, json=json_data)
    return response_with_models_info


def get_response_with_prices_info(params, url='https://www.mvideo.ru/bff/products/prices'):
    response_with_prices_info = requests.get(url, cookies=cookies, headers=headers, params=params)
    return response_with_prices_info
