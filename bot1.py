import telebot

bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я бот автопродаж. Что ты хочешь купить?')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'автомобиль':
        bot.send_message(message.chat.id, 'У нас есть много моделей автомобилей. Какую модель ты хочешь купить?')
    elif message.text.lower() == 'мотоцикл':
        bot.send_message(message.chat.id, 'У нас есть много моделей мотоциклов. Какую модель ты хочешь купить?')
    else:
        bot.send_message(message.chat.id, 'Извини, я не понимаю. Попробуй еще раз.')

bot.polling()
