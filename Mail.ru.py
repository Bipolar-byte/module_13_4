from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import random

api = ""

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

health_tips = [
    "Пейте больше воды каждый день.",
    "Регулярно занимайтесь физическими упражнениями.",
    "Старайтесь спать не менее 7-8 часов каждую ночь.",
    "Питайтесь разнообразно и включайте в рацион свежие фрукты и овощи.",
    "Регулярно делайте перерывы во время работы для отдыха глаз и тела."
]

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Привет! Я бот, помогающий твоему здоровью. Введите /help, чтобы узнать доступные команды.")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    help_text = (
        "Я помогу тебе заботиться о здоровье!\n"
        "Доступные команды:\n"
        "/start - начать общение с ботом\n"
        "/help - получить список команд\n"
        "/tips - получить случайный совет по здоровью\n"
        "/about - узнать больше обо мне\n"
        "/calories - рассчитать норму калорий."
    )
    await message.reply(help_text)

@dp.message_handler(commands=["tips"])
async def tips_command(message: types.Message):
    tip = random.choice(health_tips)
    await message.reply(tip)

@dp.message_handler(commands=["about"])
async def about_command(message: types.Message):
    about_text = (
        "Я бот, созданный, чтобы помогать вам заботиться о здоровье. "
        "Я могу давать советы, напоминать о важности отдыха и физической активности. "
        "Надеюсь быть полезным!"
    )
    await message.reply(about_text)

@dp.message_handler(commands=["calories"])
async def set_age(message: types.Message):
    await UserState.age.set()
    await message.answer("Введите свой возраст:")

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer("Введите свой рост:")

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer("Введите свой вес:")

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в день.")
    await state.finish()

@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo_message(message: types.Message):
    await message.reply(message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
