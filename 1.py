import dp as dp
import telebot
import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = telebot.TeleBot('5117734670:AAEHIuwpvczFayX96aQ5KpbwfDZIMtQVN6w')

# Приветственное сообщение
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветы! Велкам на треню по импровизации.\nПравила просты как 2Х2 (не канал):\n1. Прочти =) плиз!\n2. Приготовься придумать прикольное продолжение ситуации.\n3. После нажатия на кнопку "ГОТОВ", У тебя 30 секунд на ответ!\n4. Чуток ждём и получаем 5 вариантов от участников.\n4. Отмечаем самый прикольный, думаем как улучшить функционал. \n 5. Воть =)')


# Подключаемся к базе данных
conn = sqlite3.connect('mydatabase.db')

# Создаем курсор для выполнения операций
cursor = conn.cursor()


# Обрабатываем команду /random_message
@dp.message_handler(commands=['random_message'])
async def send_random_message(message: types.Message):
    # Выполняем запрос для получения случайного предложения из таблицы sentences
    cursor.execute('SELECT sentence FROM sentences ORDER BY RANDOM() LIMIT 1')
    row = cursor.fetchone()

    # Отправляем случайное предложение пользователю
    await message.answer(row[0])


# Обрабатываем ошибки
@dp.errors_handler()
async def error_handler(update, exception):
    print(f'Exception occured: {exception}')


# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
