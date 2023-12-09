from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from ..states import ClientStatesGroup
from bot.quiz_bot import dp
from db import Users


@dp.message(Command("start"))
async def quit_handler(message: types.Message, state: FSMContext):
    await state.set_state(ClientStatesGroup.default)
    Users.add_user(user_id=message.from_user.id)
    await message.answer("Hi there!")


@dp.message(Command("quit"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.set_state(ClientStatesGroup.default)
    await message.answer("Action quit with success")


@dp.message(Command("quiz"), ClientStatesGroup.default)
async def start_random_quiz_handler(message: types.Message, state: FSMContext):
    await state.set_state(ClientStatesGroup.random_quiz)
    await message.answer("Starting a random quiz. Choose the number of questions and architectural types.")


@dp.message()
async def default_handler(message: types.Message):
    await message.answer("You are not registered yet( \n Please enter /start command")
