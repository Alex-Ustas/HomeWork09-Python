import telebot
import bot_api

# Name: CandyGame
# Bot name: alexhomework09_bot

bot = telebot.TeleBot(bot_api.TOKEN)
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

@bot.message_handler(commands=['help'])
def game_help(message):
    bot.send_message(message.chat.id, game_desc, parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Начало игры')


bot.polling()
