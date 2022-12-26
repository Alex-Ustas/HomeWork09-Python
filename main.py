import telebot
import bot_api
from random import choice
from random import randint

# Name: CandyGame
# Bot name: alexhomework09_bot

bot = telebot.TeleBot(bot_api.TOKEN)
game_desc = """
*Условие игры:*
На столе лежит 117 конфет.
Играют два игрока делая ход друг после
друга. Первый ход определяется
жеребьёвкой. За один ход можно
забрать не более чем 28 конфет.
Все конфеты оппонента достаются
сделавшему *последний ход*.
Для начала игры напишите [/start]"""

candies = dict()
enable_game = dict()
turn = dict()


def handle_game_proc(message):
    global enable_game
    try:
        if enable_game[message.chat.id] and 1 <= int(message.text) <= 28:
            return True
        else:
            return False
    except ValueError or KeyError:
        bot.reply_to(message, 'Неверный ввод!')


@bot.message_handler(commands=['help'])
def game_help(message):
    bot.send_message(message.chat.id, game_desc, parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global turn, candies, enable_game
    bot.reply_to(message, 'Начинаем!')
    enable_game[message.chat.id] = True
    candies[message.chat.id] = 117
    turn[message.chat.id] = choice(['Bot', 'User'])
    bot.send_message(message.chat.id, f'Итого 117 конфет. Начинает {turn[message.chat.id]}')
    if turn[message.chat.id] == 'Bot':
        take = randint(1, candies[message.chat.id] % 29)
        candies[message.chat.id] -= take
        bot.send_message(message.chat.id, f'Бот взял {take}')
        bot.send_message(message.chat.id, f'Осталось {candies[message.chat.id]}')
        turn[message.chat.id] = 'User'


@bot.message_handler(func=handle_game_proc)
def game_process(message):
    global candies, turn, enable_game
    candies[message.chat.id] -= int(message.text)
    bot.send_message(message.chat.id, f'Осталось {candies[message.chat.id]}')
    if candies[message.chat.id] % 29 == 0:
        take = randint(1, 28)
        candies[message.chat.id] -= take
        bot.send_message(message.chat.id, f'Бот взял {take}')
        bot.send_message(message.chat.id, f'Осталось {candies[message.chat.id]}, ваш ход')
        if candies[message.chat.id] <= 28:
            bot.send_message(message.chat.id, f'User взял {candies[message.chat.id]}')
            bot.send_message(message.chat.id, 'User Win')
            enable_game[message.chat.id] = False
    elif candies[message.chat.id] > 28:
        take = candies[message.chat.id] % 29
        candies[message.chat.id] -= take
        bot.send_message(message.chat.id, f'Бот взял {take}')
        bot.send_message(message.chat.id, f'Осталось {candies[message.chat.id]}, ваш ход')
    else:
        bot.send_message(message.chat.id, f'Бот взял {candies[message.chat.id]}')
        bot.send_message(message.chat.id, 'Bot Win')
        enable_game[message.chat.id] = False


bot.polling()
