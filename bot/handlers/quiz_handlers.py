from aiogram import types
from ..states import ClientStatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.quiz_bot import dp


@dp.message(Command("start"))
async def quit_handler(message: types.Message, state: FSMContext):
    await state.set_state(ClientStatesGroup.default)
    await message.answer("Hi there!")


@dp.message(Command("quit"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.set_state(ClientStatesGroup.default)
    await message.answer("Action quit with success")


@dp.message(Command("quiz"))
async def start_random_quiz(message: types.Message, state: FSMContext):
    await state.set_state(ClientStatesGroup.random_quiz)
    await message.answer("Starting a random quiz. Choose the number of questions and architectural types.")


@dp.message(Command("create_quiz"))
async def create_quiz(message: types.Message, state: FSMContext):
    await state.set_state(ClientStatesGroup.random_quiz)
    await message.answer("Creating a quiz. Use /addquestion to add questions and /finishquiz to finish.")
