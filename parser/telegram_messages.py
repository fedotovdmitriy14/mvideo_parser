import telebot

from mvideo_parser import MvideoParser
from settings import TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)

parser = MvideoParser()


def get_all_sales():
    return parser.get_all_discounts_today()


@bot.message_handler(commands=['sales'])
def send_welcome(message):
    tv_on_sale = get_all_sales()
    for tv in tv_on_sale:
        bot.reply_to(message, tv)


bot.infinity_polling()
