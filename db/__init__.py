import psycopg2
import json

from quiz.quiz import Question, Quiz


class DataBase:
    def __init__(self, db_params):
        self._connection = psycopg2.connect(**db_params)

    def disconnect(self):
        self._connection.close()

    def _execute_no_fetch(self, query: str):
        cursor = self._connection.cursor()
        cursor.execute(query)
        self._connection.commit()
        cursor.close()

    def _execute_all(self, query: str):
        cursor = self._connection.cursor()
        cursor.execute(query)
        ans = cursor.fetchall()
        self._connection.commit()
        cursor.close()

        return ans

    def _execute(self, query: str):
        cursor = self._connection.cursor()
        cursor.execute(query)
        ans = cursor.fetchone()
        self._connection.commit()
        cursor.close()

        return ans


class QuestionsDB(DataBase):
    def get_question(self, question_id: int) -> Question:
        ans = None
        try:
            ans = self._execute(
                f"""
                SELECT * 
                FROM "Questions" AS q
                WHERE q.question_id = {question_id};
                """)

            return Question(*ans)
        except Exception as e:
            print(f"Error: {e}")

        return ans

    def get_random_questions(self, n: int) -> list[Question]:
        ans = None
        try:
            ans = self._execute_all(
                f"""
                SELECT *
                FROM "Questions" AS q
                ORDER BY RANDOM()
                LIMIT {n};
                """)

            return [Question(q[1], q[5], q[2], q[3], q[4]) for q in ans]
        except Exception as e:
            print(f"Error: {e}")


    def add_question(self, question: Question) -> bool:
        try:
            self._execute_no_fetch(
                f"""
                INSERT INTO "Questions" (
                title, description, image_url, variants, answer
                )
                VALUES ('{question.title}', '{question.description}', '{question.image_url}', '{json.dumps(question.variants)}'::jsonb, '{question.answer}');
                """)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def delete_question(self, question_id: int):
        try:
            self._execute_no_fetch(
                f"""
                DELETE FROM "Questions"
                WHERE question_id = {question_id}
                """
            )[0]

            return True
        except Exception as e:
            print(f"Error: {e}")

            return False

    def get_len(self) -> int:
        ans = ()
        try:
            ans = self._execute(
                f"""
                SELECT COUNT(*)
                FROM "Questions";
                """
            )
        except Exception as e:
            print(f"Error: {e}")

        return ans[0]

    def __len__(self):
        return self.get_len()


cfg = json.load(open("config.json"))
Questions = QuestionsDB(cfg["db_params"])
