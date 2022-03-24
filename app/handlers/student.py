from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.models.User import *


available_actions = ["пройти тест", "посмотреть статистику"]  #
available_tests = ["тест 1", "тест 2", "тест 3"]  # тут из бд нужно


class StudentActions(StatesGroup):
    waiting_for_action = State()
    waiting_for_test = State()


async def student_start(message: types.Message):
    try:
        user = User.get(User.id == message.from_user.id)
        await message.answer("я тебя уже видел")
    except DoesNotExist:
        #await StudentActions.waiting_for_action.set()
        await message.answer("Я тебя еще не видел")
        User.create(id=message.from_user.id, firstname="student", secondname="kk")


# Обратите внимание: есть второй аргумент
async def action_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_actions:
        await message.answer("Выберите дейстивие, используя клавиатуру ниже")
        return

    User.create(id=message.from_user.id, name=message.text)
    await state.finish()

async def test_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_tests:
        await message.answer("Пожалуйста, выберите действие, испльзуя клавиатуру ниже")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы выбрали {message.text.lower()} кнопкой {user_data['chosen_action']}.\n",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(student_start, commands="student", state="*")
    dp.register_message_handler(action_chosen, state=StudentActions.waiting_for_action)
    dp.register_message_handler(test_chosen, state=StudentActions.waiting_for_test)
