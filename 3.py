import random
import sqlite3
import time
import logging

import states as state
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType

# Установка уровня логов
logging.basicConfig(level=logging.INFO)

# Токен бота
BOT_TOKEN = '5117734670:AAEHIuwpvczFayX96aQ5KpbwfDZIMtQVN6w'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Состояния бота
class Form(StatesGroup):
    ready = State()
    feedback = State()


# Инициализация базы данных и создание таблиц
conn = sqlite3.connect('feedback.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              message TEXT,
              rating INTEGER)''')
conn.commit()


# Получение рандомного сообщения из базы данных
def get_random_message():
    c.execute("SELECT message FROM messages ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()
    return result[0] if result else None


# Сохранение сообщения и времени его отправки в состояние FSM
async def set_message_data(state: FSMContext, message_id: int):
    message_sent_time = time.time()
    await state.update_data(message_id=message_id, message_sent_time=message_sent_time)


# Получение сообщения и времени его отправки из состояния FSM
async def get_message_data(state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    message_sent_time = data.get('message_sent_time')
    return message_id, message_sent_time


# Получение оценок из базы данных и отправка пользователю для оценки
async def send_ratings(chat_id: int, message_id_list: list):
    ratings_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    ratings_keyboard.add("1", "2", "3", "4", "5")

    # Получение трех случайных сообщений из базы данных
    c.execute("SELECT id, message FROM messages WHERE id IN (?, ?, ?)",
              random.sample(message_id_list, k=3))
    result = c.fetchall()

    # Отправка пользователю трех сообщений для оценки
    for row in result:
        message_id, message = row
        await bot.send_message(chat_id, message, reply_markup=ratings_keyboard)
        await set_message_data(Form.feedback, message_id)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    ready_button = types.KeyboardButton(text="Готов")
    keyboard.add(ready_button)
    await message.reply("Привет! Нажми на кнопку \"Готов\", когда будешь готов начать.", reply_markup=keyboard)
    await Form.ready.set()


# Обработчик нажатия на кнопку
@dp.message_handler(states=state.RATING)
async def process_rating(message: types.Message, state: FSMContext, RATING_TIMEOUT=None):
    # Получаем состояние FSM
    state_data = await state.get_data()
    data = state_data.get('data', {})

    # Обновляем словарь с данными
    data['rating'] = message.text

    # Обновляем состояние FSM
    await state.update_data(data)

    # Получаем ID сообщения и время отправки из состояния FSM
    message_id = state_data.get('message_id')
    message_sent_time = state_data.get('message_sent_time')

    # Вычисляем время, прошедшее с отправки сообщения
    elapsed_time = time.time() - message_sent_time

    # Проверяем, что время ответа не истекло
    if elapsed_time > RATING_TIMEOUT:
        await bot.send_message(message.chat.id, "Время на оценку сообщений истекло!")
        await state.finish()
        return

    # Переходим к следующему сообщению для оценки
    message_id_list = state_data.get('message_id_list')
    message_id_list.remove(message_id)

    if message_id_list:
        # Обновляем состояние FSM
        await state.update_data({'message_id_list': message_id_list})
        await ask_rating(message.chat.id, message_id_list[0], state)
    else:
        # Сохраняем результаты оценки в БД
        await save_ratings(state_data, message.from_user.id)

        # Оповещаем пользователя об окончании оценки
        await bot.send_message(message.chat.id, "Спасибо за участие!")

        # Завершаем состояние FSM
        await state.finish()
