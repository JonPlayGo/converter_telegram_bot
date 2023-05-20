from aiogram import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from mytoken import token
from currency_converter import CurrencyConverter
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
c = CurrencyConverter()

class Converting(StatesGroup):
    start_convert = State()
    second_currency = State()
    final = State()


@dp.message_handler(commands="start",state="*")
async def start(message: types.Message,state: FSMContext):
    await message.answer("Input currency for convert")
    await Converting.start_convert.set()

@dp.message_handler(state=Converting.start_convert)
async def input_second_currency(message: types.Message):
    global first_currency
    first_currency = message.text
    await message.answer("Input second currency")
    await Converting.second_currency.set()

@dp.message_handler(state=Converting.second_currency)
async def amout_of_currency(message: types.Message):
    global second_currency
    second_currency = message.text
    await message.answer("Input amount of currency")
    await Converting.final.set()

@dp.message_handler(state=Converting.final)
async def final(message: types.Message):
    amout_of_currency = message.text
    try:
        amout_of_currency = int(amout_of_currency)
        result = c.convert(amout_of_currency,first_currency,second_currency)
        await message.answer(f"result : {result}")
    except:
        await message.answer("Input integer")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)