from aiogram.fsm.state import State, StatesGroup


class ClientStatesGroup(StatesGroup):
    default = State()
    random_quiz = State()
    question_num = State()
    quiz_answer = State()
    get_result = State()
