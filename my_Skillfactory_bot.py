import telebot
from config import TOKEN, exchanges
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Приветствую Вас, в конвертере валют!\n \
Чтобы начать работу введите команду боту через пробел в формате:\n<наименование валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\
Например: доллар рубль 100\n\
Чтобы узнать доступные валюты, введите или нажмите: /values"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.lower().split()
    try:
        if len(values) != 3:
            raise APIException("Неверное количество параметров, должно быть 3")
        base, quote, amount = values
        total_price = Converter.get_price(*values)
        total_price = round(total_price, 2)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка запроса.\n{e}")
    else:
        text = f"Цена {amount} {base} в {quote} = {total_price}"
        bot.send_message(message.chat.id, text)

bot.polling()
