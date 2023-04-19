import sqlite3
import random
import asyncio
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create the Telegram bot object
bot = Bot(token='5117734670:AAEHIuwpvczFayX96aQ5KpbwfDZIMtQVN6w')
dp = Dispatcher(bot)

# Define the start command handler
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Send a welcome message and a "READY" button to the user
    ready_button = KeyboardButton('READY')
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(ready_button)
    await message.answer('Welcome! Press the button below when you are ready to continue.', reply_markup=markup)

# Define the READY button handler
@dp.message_handler(text='READY')
async def ready_handler(message: types.Message):
    # Select a random sentence from the database
    cursor.execute('SELECT sentence FROM sentences ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    sentence = result[0] if result else 'No sentences found.'
    # Send the sentence to the user
    await message.answer(md.text(md.bold('Here is your random sentence:'), md.code(sentence)))

if __name__ == '__main__':
    # Start the bot
    asyncio.run(dp.start_polling())
