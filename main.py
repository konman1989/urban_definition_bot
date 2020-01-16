import re
import requests
from telebot import TeleBot, types


bot = TeleBot('982217890:AAHU7pedco6HUQfIUy_nqR2EyPQ3pjVS2WE')
markup = types.ReplyKeyboardMarkup(row_width=2)

@bot.message_handler()
def get_definition(message):
    req = requests.get(
        f'http://api.urbandictionary.com/v0/define?term={message.text}")')

    text = ""

    for _ in req.json().get('list'):
        text += _.get('definition')

    result = re.finditer(r'\[\w+\]', text)

    bot.send_message(message.chat.id, text)

    definitions = []

    for _ in result:
        definitions.append(_.group()[1:-1])

    # for item in range(0, 12, 3):
    #     word1 = types.KeyboardButton(definitions[item])
    #     word2 = types.KeyboardButton(definitions[item + 1])
    #     word3 = types.KeyboardButton(definitions[item + 2])
    #     markup.row(word1, word2, word3)

    for word in definitions[:10]:
        word = types.KeyboardButton(word)
        markup.add(word)

    bot.send_message(message.chat.id, "Choose a word:",
                     reply_markup=markup)

    req = requests.get(
        f'http://api.urbandictionary.com/v0/define?term={message.text}")')

    text = ""

    for _ in req.json().get('list'):
        text += _.get('definition')

    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling()