from collections import Counter

from bot.quiz_bot import bot
from db import QuestionAnswerDetails


async def show_stats(chat_id, user_id: int):
    stats = QuestionAnswerDetails.get_stats(user_id)
    if len(stats) == 0:
        await bot.send_message(chat_id, "Вы пока еще не ответили ни на один вопрос🤡")
    right_guessed = sum([1 if i[1] else 0 for i in stats])
    false_guessed = sum([0 if i[1] else 1 for i in stats])
    answers = [i[7][i[8]] for i in stats]
    counter = Counter(answers)
    most_guessed_style = Counter.most_common(counter)[0]
    perc = (100 * right_guessed) // (right_guessed + false_guessed)

    stats_message = \
        f"""
    Краткая статистика:
    Вы ответили правильно на {right_guessed} вопр. 👑
    Ошиблись в ответах на  {false_guessed} вопр. 👹
    Ваш процент правильных ответов составляет {perc}% {judge_result(perc, 100)}
    Самый частый ответ на вопрос: {most_guessed_style[0]} - {most_guessed_style[1]} раз
    """
    await bot.send_message(chat_id, stats_message)


def judge_result(points: int, max_points: int) -> str:
    if points / max_points < 0.6:
        return "🤮"
    elif 0.6 <= points / max_points < 0.75:
        return "😐"
    elif 0.75 <= points / max_points < 0.9:
        return "😙"
    else:
        return "🤩"
