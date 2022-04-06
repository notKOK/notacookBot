from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.dispatcher.filters import Text
from app.config_reader import load_config
from app.models.User import *

db.connect()
db.create_tables([User])

config = load_config("config/bot.ini")

available_actions = ["статистика", "загрузить статистику", "загрузить новый тест"]
available_smth = ["empty"]
existing_names = {config.tg_bot.admin_id}


class TeacherMoves(StatesGroup):
    waiting_for_enter_name = State()
    waiting_for_actions = State()
    waiting_for_smth = State()


async def enter_name(message: types.Message):
    try:
        user = User.get(User.id == message.from_user.id)
        await message.answer(user.id)
    except DoesNotExist:
        User.create(id=message.from_user.id, firstname="dlfjak", secondname="asdf")
        await message.answer("Ты в базе")


async def action_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_actions:
        keyboard.add(name)
    await message.answer("Выберите действие:", reply_markup=keyboard)
    await TeacherMoves.waiting_for_actions.set()


async def action_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_actions:
        await message.answer("Пожалуйста, выберите дейсвие, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_smth=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_smth:
        keyboard.add(size)
    # для простых шагов можно не указывать название состояния, обходясь next()
    await TeacherMoves.next()
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


async def another_action_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_smth:
        await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы выбрали {user_data['chosen_smth']} кнопкой {message.text.lower()}.\n"
                         f"Попробуйте теперь стать студентом /student - у вас ничего не получится",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_teacher(dp: Dispatcher):
    dp.register_message_handler(action_start, commands="action", state="*")
    dp.register_message_handler(enter_name, Text(equals="Преподаватель", ignore_case=True), state="*")
    dp.register_message_handler(action_chosen, state=TeacherMoves.waiting_for_actions)
    dp.register_message_handler(another_action_chosen, state=TeacherMoves.waiting_for_smth)
