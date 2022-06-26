from environs import Env


env = Env()

TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
print(TELEGRAM_TOKEN)