import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# создаем бота и указываем токен
bot = telebot.TeleBot('5117734670:AAEHIuwpvczFayX96aQ5KpbwfDZIMtQVN6w')

# создаем клавиатуру с кнопкой "Готов"
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
ready_button = KeyboardButton('Готов')
keyboard.add(ready_button)


# обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # отправляем приветственное сообщение и клавиатуру с кнопкой "Готов"
    bot.reply_to(message, 'Приветы! Велкам на треню по импровизации.\nПравила просты как 2Х2 (не канал):\n1. Прочти =) плиз!\n2. Приготовься придумать прикольное продолжение ситуации.\n3. После нажатия на кнопку "ГОТОВ", У тебя 60 секунд на ответ!\n4. После ввода продолжения, посмотри ответы других.\n5. Отметь самый прикольный по 5-тибалльной шкале. \n6. Чао! =)', reply_markup=keyboard)


# обработчик кнопки "Готов"
@bot.message_handler(func=lambda message: message.text == 'Готов')
def ready(message):
    # отправляем рандомное предложение
    bot.reply_to(message, "Вот твое рандомное предложение: ...")


# запускаем бота
bot.polling()
