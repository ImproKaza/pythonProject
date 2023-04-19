from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# создание объекта бота
bot = Bot(token="5117734670:AAEHIuwpvczFayX96aQ5KpbwfDZIMtQVN6w")

# создание объекта диспетчера
dp = Dispatcher(bot)

# создание хэндлера для обработки команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Приветы! Велкам на треню по импровизации.\nПравила просты как 2Х2 (не канал):\n1. Прочти =) плиз!\n2. Приготовься придумать прикольное продолжение ситуации.\n3. После нажатия на кнопку "ГОТОВ", У тебя 60 секунд на ответ!\n4. После ввода продолжения, посмотри ответы других.\n5. Отметь самый прикольный по 5-тибалльной шкале. \n6. Чао! =)')



# запуск бота
executor.start_polling(dp)
