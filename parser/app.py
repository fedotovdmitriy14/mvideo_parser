import schedule

from mvideo_parser import MvideoParser

parser = MvideoParser()


def run_all_methods():
    print(parser.get_json_data_and_params_from_products_ids())
    print(parser.add_model_name_and_link_to_tv_info())
    print(parser.add_prices_to_tv_info())


schedule.every(30).seconds.do(run_all_methods)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
