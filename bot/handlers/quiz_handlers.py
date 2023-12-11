from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..states import ClientStatesGroup
from ..Stats import show_stats
from bot.quiz_bot import dp, bot
from db import Users


@dp.message(Command("help"))
async def help_handler(message: types.Message):
    commands = """
    Доступные команды:
    /start - стартовая команда\n
    /quit - выйти из текущего состояния в изначальное\n
    /quiz - начать случайную викторину\n
    /stats - вывести статистику
    """
    await bot.send_message(message.chat.id, commands)


@dp.message(Command("start"))
async def quit_handler(message: types.Message, state: FSMContext):
    await state.set_state(ClientStatesGroup.default)
    Users.add_user(user_id=message.from_user.id)
    await message.answer("Привет!\nОтправьте команду /help чтобы посмотреть возможности бота")


@dp.message(Command("quit"))
async def start_handler(message: types.Message, state: FSMContext):
    if await state.get_state() == ClientStatesGroup.default:
        await bot.send_message(message.chat.id, "Вы уже в главном меню")
    elif await state.get_state() is None:
        await bot.send_message(message.chat.id, "Сначала нажмите введите команду /start")
    else:
        await state.set_state(ClientStatesGroup.default)
        await bot.send_message(message.chat.id, "Вы успешно вышли")


@dp.message(Command("quiz"), ClientStatesGroup.default)
async def start_random_quiz_handler(message: types.Message, state: FSMContext):
    await state.set_state(ClientStatesGroup.random_quiz)

    builder = InlineKeyboardBuilder()
    builder.button(text='✅', callback_data="Да")
    builder.button(text='❌', callback_data="Нет")

    await bot.send_message(message.chat.id, "Создать викторину без вопросов, на которые вы уже отвечали?",
                           reply_markup=builder.as_markup())


@dp.message(Command("stats"), ClientStatesGroup.default)
async def start_random_quiz_handler(message: types.Message, state: FSMContext):
    await show_stats(message.chat.id, message.from_user.id)


@dp.message()
async def default_handler(message: types.Message):
    await message.answer(
        "Такой команды не существует или вы еще не нажали /start. Чтобы посмотреть все команды введите /help")
