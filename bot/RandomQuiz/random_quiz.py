from aiogram.types import CallbackQuery

from bot.quiz_bot import dp
from ..Quiz import *


@dp.message(ClientStatesGroup.random_quiz)
async def starting_random_quiz(message: types.Message, state: FSMContext):
    await start_random_quiz(message, state)


@dp.callback_query(ClientStatesGroup.quiz_answer)
async def answering_random_quiz(query: CallbackQuery, state: FSMContext):
    await answer_random_quiz(query.message.chat.id, query.data, state)
