from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from dispatcher import dp
from aiogram.dispatcher.filters.state import State, StatesGroup
import students

available_roles = ["Студент", "Преподавтель"]


class UserActions(StatesGroup):
    waiting_for_student = State()
    waiting_for_teacher = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_roles:
        keyboard.add(name)
    await message.answer("Привет, вы студет или преподаватель?", reply_markup=keyboard)


async def role_chosen(message: types.Message, state: FSMContext):
    if message.text.lowe() not in available_roles:
        await message.answer("Выберите действие, используя клавиатуру ниже")
        return
    await state.update_data(chosen_actrion=message.text.lower())


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(students.student_start, state=UserActions.waiting_for_student)
    dp.register_message_handler(students.student_start, state=UserActions.waiting_for_student)

