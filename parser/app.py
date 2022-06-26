import schedule

from mvideo_parser import MvideoParser

parser = MvideoParser()


def run_all_methods():
    print(parser.get_all_discounts_today())


schedule.every(30).seconds.do(run_all_methods)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
