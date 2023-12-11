from aiogram.types import CallbackQuery, Message

from bot.quiz_bot import dp
from ..Quiz import *


@dp.callback_query(ClientStatesGroup.random_quiz)
async def starting_random_quiz(query: CallbackQuery, state: FSMContext):
    await start_random_quiz(query, state)


@dp.message(ClientStatesGroup.question_num)
async def set_q_num(message: Message, state: FSMContext):
    await set_questions_num(message, state)


@dp.callback_query(ClientStatesGroup.quiz_answer)
async def answering_random_quiz(query: CallbackQuery, state: FSMContext):
    await answer_random_quiz(query.from_user.id, query.message.chat.id, query.message.message_id, query.data, state)
