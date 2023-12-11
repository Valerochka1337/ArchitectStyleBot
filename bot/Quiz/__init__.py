from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from datetime import datetime

from bot.quiz_bot import bot
from ..states import ClientStatesGroup
from db import Questions, QuestionAnswerDetails

INVALID_IMAGE_URL = "https://static.vecteezy.com/system/resources/previews/005/337/799/non_2x/icon-image-not-found-free-vector.jpg"


async def start_random_quiz(query: CallbackQuery, state: FSMContext):
    await state.set_state(ClientStatesGroup.question_num)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    if query.data == "Да":
        await state.update_data(unans=True)
    else:
        await state.update_data(unans=False)
    await bot.send_message(query.message.chat.id, "Введите желаемое число вопросов:")


async def set_questions_num(message: Message, state: FSMContext):
    try:
        questions_num = int(message.text)
    except Exception as e:
        print(f"Error {e}")
        await message.answer("Это не число!")
        return
    max_questions_num = len(Questions)
    data = await state.get_data()
    if data.get('unans', False):
        max_questions_num = len(Questions.get_unanswered_random_questions(questions_num, message.from_user.id))
    if 0 <= max_questions_num < questions_num:
        await bot.send_message(message.chat.id,
                               f"Не получилось составить викторину из {questions_num} вопр.! Всего доступно только {max_questions_num} вопр.")
        await state.set_state(ClientStatesGroup.default)
        return
    else:
        await bot.send_message(message.chat.id, f"Вы начали викторину из {questions_num} вопр.!")

    if data.get('unans', False):
        questions = Questions.get_unanswered_random_questions(questions_num, message.from_user.id)
    else:
        questions = Questions.get_random_questions(questions_num)

    await state.set_state(ClientStatesGroup.quiz_answer)
    await state.update_data(questions=questions, right_answer=None, question_num=1, start_date=datetime.now())
    await answer_random_quiz(message.from_user.id, message.chat.id, message.message_id, "", state)


async def answer_random_quiz(user_id, chat_id, message_id, query_data, state: FSMContext):
    questions_data = await state.get_data()
    questions = questions_data.get('questions', [])
    right_answer = questions_data.get('right_answer', "")
    question_num = questions_data.get('question_num', 0)
    if right_answer:
        QuestionAnswerDetails.add_answer(datetime.now(), user_id, query_data == right_answer,
                                         questions[question_num - 2].question_id)
        builder = InlineKeyboardBuilder()
        question = questions[question_num - 3]
        for num, answer in question.variants.items():
            await state.set_state(ClientStatesGroup.quiz_answer)
            s = ""
            if str(num) == query_data:
                if query_data == right_answer:
                    s = ' ✅'
                else:
                    s = ' ❌'
            builder.button(text=str(answer) + s, callback_data=str(num))
        await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=builder.as_markup())

    if len(questions) == question_num - 1:
        await state.set_state(ClientStatesGroup.get_result)
        await get_result(user_id, chat_id, state)
        return

    builder = InlineKeyboardBuilder()
    question = questions[question_num - 2]
    for num, answer in question.variants.items():
        await state.set_state(ClientStatesGroup.quiz_answer)
        builder.button(text=str(answer), callback_data=str(num))
    await state.update_data(questions=questions,
                            right_answer=question.answer,
                            question_num=question_num + 1)

    await bot.send_message(chat_id, f"{question_num}) {question.title}")
    try:
        await bot.send_photo(chat_id, question.image_url, caption=question.description,
                             reply_markup=builder.as_markup())
    except Exception as e:
        print(f"Error: {e}")
        await bot.send_photo(chat_id, INVALID_IMAGE_URL, caption=question.description,
                             reply_markup=builder.as_markup())


async def get_result(user_id, chat_id, state: FSMContext):
    questions_data = await state.get_data()
    date = questions_data.get('start_date', "")
    res = QuestionAnswerDetails.get_questions_from_date(user_id, date)
    await state.set_state(ClientStatesGroup.default)

    points = sum([1 if bool(a[1]) else 0 for a in res])
    max_points = len(res)
    await bot.send_message(chat_id, judge_result(points, max_points))
    await bot.send_message(chat_id, f"Ваш результат: {points}/{max_points}")


def judge_result(points: int, max_points: int) -> str:
    if points / max_points < 0.6:
        return "Ужас! 🤮🤮🤮"
    elif 0.6 <= points / max_points < 0.75:
        return "Пойдет. 😐😐😐"
    elif 0.75 <= points / max_points < 0.9:
        return "Хорошо! 😙😙😙"
    else:
        return "Отлично! 🤩🤩🤩"
