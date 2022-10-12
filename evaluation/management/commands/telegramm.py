from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
from evaluation.models import People
from telebot.apihelper import ApiTelegramException

token = '5428275165:AAFiYgcbBWndBrdd4sjmz6XVQVlw6FGqdUg'

MypyBot = TeleBot(token, threaded=False)


@MypyBot.message_handler(commands=['start'])
def start_message(message):
    MypyBot.send_message(message.chat.id, "Привет ✌ \nЭто бот для отслеживания отзывов ")
    if not People.objects.filter(telegram_id=message.chat.id).exists():
        People.objects.create(telegram_id=message.chat.id, first_name=message.chat.first_name, username=message.chat.username)


def send_message(message, id_list):
    sent = list()

    for tg_id in id_list:
        try:
            sent.append(MypyBot.send_message(tg_id, message))
        except ApiTelegramException as e:
            if e.description == "Forbidden: bot was blocked by the user":
                print("The user {} has blocked the bot. I can't send anything to them".format(
                    tg_id))
    return sent


def update_message(text, dict_sent):
    for key, value in dict_sent.items():
        MypyBot.edit_message_text(text, key, value)


class Command(BaseCommand):
    help = 'It is bot command'

    def handle(self, *args, **kwargs):
        try:
            MypyBot.polling()
        except Exception as e:
            print(f'Error {e}')











