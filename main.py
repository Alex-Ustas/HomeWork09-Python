import telebot
import bot_api
from random import choice
from random import randint

# Name: CandyGame
# Bot name: alexhomework09_bot

bot = telebot.TeleBot(bot_api.TOKEN)
bot_name = bot.user.first_name
game_desc = """
*Условие игры:* На столе лежит 117 конфет. Играют два
игрока делая ход друг после друга. Первый ход определяется
жеребьёвкой. За один ход можно забрать не более чем 28
конфет. Все конфеты оппонента достаются сделавшему
*последний ход*.
Для начала игры напишите [/start]"""

candy = dict()
enable_game = dict()
turn = dict()


def handle_game_proc(message):
    global enable_game
    try:
        if enable_game[message.chat.id] and 1 <= int(message.text) <= 28:
            return True
        else:
            return False
    except KeyError:
        enable_game[message.chat.id] = False
        if enable_game[message.chat.id] and 1 <= int(message.text) <= 28:
            return True
        else:
            return False


@bot.message_handler(commands=['help'])
def game_help(message):
    bot.send_message(message.chat.id, game_desc, parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global turn, candy, enable_game
    bot.reply_to(message, 'Начинаем!')
    enable_game[message.chat.id] = True
    candy[message.chat.id] = 117
    turn[message.chat.id] = choice(['Bot', 'User'])
    bot.send_message(message.chat.id, f'Начинает {turn[message.chat.id]}')
    if turn[message.chat.id] == 'Bot':
        take = randint(1, candy[message.chat.id] % 29)
        candy[message.chat.id] -= take
        bot.send_message(message.chat.id, f'Бот взял {take}')
        bot.send_message(message.chat.id, f'Осталось {candy[message.chat.id]}')
        turn[message.chat.id] = 'User'


@bot.message_handler(func=handle_game_proc)
def game_process(message):
    global candy, turn, enable_game
    if turn[message.chat.id] == 'User':
        if candy[message.chat.id] > 28:
            candy[message.chat.id] -= int(message.text)
            bot.send_message(message.chat.id,
                             f'Осталось {candy[message.chat.id]}')
            if candy[message.chat.id] > 28:
                take = randint(1, candy[message.chat.id] % 29)
                candy[message.chat.id] -= take
                bot.send_message(message.chat.id,
                                 f'Бот взял {take}')
                bot.send_message(message.chat.id,
                                 f'Осталось {candy[message.chat.id]}')
                if candy[message.chat.id] <= 28:
                    bot.send_message(message.chat.id, 'User Win')
                    enable_game[message.chat.id] = False
            else:
                bot.send_message(message.chat.id, 'Bot Win')
                enable_game[message.chat.id] = False
        else:
            bot.send_message(message.chat.id, 'Bot Win')
            enable_game[message.chat.id] = False


bot.polling()
