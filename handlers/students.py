from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from commands import available_roles
from commands import UserActions


available_actions = ["пройти тест", "посмотреть статистику"]  #
available_tests = ["тест 1", "тест 2", "тест 3"]  # тут из бд нужно


class StudentActions(StatesGroup):
    waiting_for_action = State()
    waiting_for_test = State()


async def student_start(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_roles:
        await message.answer("Выберите действие, используя клавиатуру ниже")
        return
    await state.update_data(chosen_action=message.text.lower())


# Обратите внимание: есть второй аргумент
async def action_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_actions:
        await message.answer("Выберите дейстивие, используя клавиатуру ниже")
        return
    await state.update_data(chosen_action=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_tests:
        keyboard.add(size)
    # Для простых шагов можно не указывать название состояния, обходясь next()
    await StudentActions.next()
    await message.answer("Номер теста:", reply_markup=keyboard)


async def test_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_tests:
        await message.answer("Пожалуйста, выберите действие, испльзуя клавиатуру ниже")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы выбрали {message.text.lower()} кнопкой {user_data['chosen_action']}.\n",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(student_start, state=UserActions.waiting_for_action)
    dp.register_message_handler(action_chosen, state=StudentActions.waiting_for_action)
    dp.register_message_handler(test_chosen, state=StudentActions.waiting_for_test)