import re
import requests
from telebot import TeleBot, types

from config import TOKEN

bot = TeleBot(TOKEN)


@bot.message_handler()
def get_definition(message):
    def text_splitter():
        """Splits text into chunks < 4096 to follow telegram message
        length rules"""

        text_list = text.split('\n')
        new_text = ""
        for chunk in text_list:
            if chunk:
                if len(new_text + chunk) < 4096:
                    new_text += "\n" + chunk
                else:
                    bot.send_message(message.chat.id,
                                     new_text.replace('Definition',
                                                      '\nDefinition'))
                    new_text = ""
                    new_text += "\n" + chunk

        bot.send_message(message.chat.id,
                         new_text.replace('Definition', '\nDefinition'))

    if message.text == '/start':
        bot.send_message(message.chat.id,
                         'Give me a definition you would like to get:')
        return
    req = requests.get(
        f'http://api.urbandictionary.com/v0/define?term={message.text}")')

    text = ""
    for index, _ in enumerate(req.json().get('list'), start=1):
        text += f"\n\nDefinition {index}:\n{_.get('definition')}"

    result = re.finditer(r'\[\w+\]', text)
    definitions = [r.group()[1:-1] for r in result]

    text = text.replace('[', '').replace(']', '')

    if len(text) > 4096:
        text_splitter()
    else:
        bot.send_message(message.chat.id, text)

    markup = types.ReplyKeyboardMarkup()

    for n in range(0, len(definitions), 3):
        buttons = (definitions[n:n + 3])
        markup.row(*buttons)

    bot.send_message(message.chat.id, '_Choose a word from the list below:_',
                     reply_markup=markup,
                     parse_mode='MarkdownV2')


if __name__ == '__main__':
    bot.polling(none_stop=True)
