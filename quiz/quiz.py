class Question:
    def __init__(self, title: str, description: str, image_url: str, variants: dict, answer: str):
        self.title = title
        self.description = description
        self.image_url = image_url
        self.variants = variants
        self.answer = answer


class Quiz:
    def __init__(self, title: str, description="Simple quiz"):
        self.title = title
        self.description = description
        self.questions: list[Question] = []

    def add_question(self, question: Question):
        self.questions.append(question)

    def delete_question(self, question: Question):
        self.questions.remove(question)
