from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from bot.quiz_bot import bot
from ..states import ClientStatesGroup
from db import Questions

INVALID_IMAGE_URL = "https://static.vecteezy.com/system/resources/previews/005/337/799/non_2x/icon-image-not-found-free-vector.jpg"


async def start_random_quiz(message: types.Message, state: FSMContext):
    try:
        questions_num = int(message.text)
    except Exception as e:
        print(f"Error {e}")
        await message.answer("Its not a number!")
        return

    if 0 < len(Questions) < questions_num:
        await bot.send_message(message.chat.id,
                               f"Can't create {questions_num} questions! Available only {len(Questions)} questions.")
        await state.set_state(ClientStatesGroup.default)
        return
    else:
        await bot.send_message(message.chat.id, f"Random quiz of {questions_num} questions started!")

    questions = Questions.get_random_questions(questions_num)

    await state.set_state(ClientStatesGroup.quiz_answer)
    await state.update_data(questions=questions, max_points=len(questions), points=0,
                            right_answer=None, question_num=1)
    await answer_random_quiz(message.chat.id, "", state)


async def answer_random_quiz(chat_id, query_data, state: FSMContext):
    questions_data = await state.get_data()
    questions = questions_data.get('questions', [])
    max_points = questions_data.get('max_points', 0)
    points = questions_data.get('points', 0)
    right_answer = questions_data.get('right_answer', "")
    question_num = questions_data.get('question_num', 0)

    if query_data == right_answer:
        points += 1

    if len(questions) == 0:
        await state.set_state(ClientStatesGroup.get_result)
        await bot.send_message(chat_id, f"You got {points}/{max_points} points")
        return

    await state.update_data(questions=questions[1:])

    builder = InlineKeyboardBuilder()
    for num, answer in questions[0].variants.items():
        await state.set_state(ClientStatesGroup.quiz_answer)
        builder.button(text=str(answer), callback_data=str(num))
    await state.update_data(questions=questions[1:], max_points=max_points, points=points,
                            right_answer=questions[0].answer, question_num=question_num + 1)

    await bot.send_message(chat_id, f"{question_num}) {questions[0].title}")
    try:
        await bot.send_photo(chat_id, questions[0].image_url, caption=questions[0].description,
                             reply_markup=builder.as_markup())
    except Exception as e:
        print(f"Error: {e}")
        await bot.send_photo(chat_id, INVALID_IMAGE_URL, caption=questions[0].description,
                             reply_markup=builder.as_markup())
