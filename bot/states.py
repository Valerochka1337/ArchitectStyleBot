from aiogram.fsm.state import State, StatesGroup


class ClientStatesGroup(StatesGroup):
    default = State()
    random_quiz = State()
    next_question = State()
    quiz_answer = State()
    get_result = State()
    custom_quiz = State()
    create_quiz = State()
