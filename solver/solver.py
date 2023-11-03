import os
from typing import Callable, Optional

import requests
from dotenv import load_dotenv

from solver.const import BASE_AUTH_URL, BASE_TASK_URL, BASE_ANSWER_URL
from solver.utils import find_dotenv


class Solver:
    def __init__(self, task) -> None:
        load_dotenv(dotenv_path=find_dotenv(os.path.dirname(os.path.abspath(__file__))))
        self.api_key: str = os.getenv("API_KEY")
        self.task: str = task
        self.url: str = BASE_AUTH_URL.format(task=task)
        self.token: Optional[str] = None
        self.input_data: Optional[dict] = None
        self.answer_from_api = None

    def authorize(self) -> None:
        data = {"apikey": self.api_key}
        response = requests.post(self.url, json=data)
        self.token = dict(response.json())["token"]

    def download_input_data(self) -> None:
        task_url = BASE_TASK_URL.format(token=self.token)
        response = requests.get(task_url)
        self.input_data = dict(response.json())

    def post_data(self, question: str):
        task_url = BASE_TASK_URL.format(token=self.token)
        question_to_send = {"question": question}
        response = requests.post(task_url, data=question_to_send)
        self.answer_from_api = dict(response.json())

    def send_answer(self, solution: Callable, **kwargs):
        if self.input_data:
            if kwargs != {}:
                answer = solution(kwargs["additional_data"])
            else:
                answer = solution(self.input_data)
        else:
            answer = solution(kwargs["question"], self.answer_from_api)

        response = requests.post(BASE_ANSWER_URL.format(token=self.token), json=answer)

        # === Verdict ===

        if response.ok:
            print("Done, answer is correct 🚀")
        else:
            print("You failed")

    def solve(self, solving_func, **kwargs):
        self.authorize()
        if kwargs == {}:
            self.download_input_data()
            self.send_answer(solving_func)
        elif "additional_data" in kwargs:
            additional_data = kwargs.get("additional_data", None)
            self.download_input_data()
            self.send_answer(solving_func, additional_data=additional_data)
        else:
            self.post_data(kwargs["question"])
            self.send_answer(solving_func, question=kwargs["question"])


if __name__ == "__main__":
    pass
