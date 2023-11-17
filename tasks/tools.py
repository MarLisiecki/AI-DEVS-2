import json

from open_ai_connector.const import OpenAiModels
from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.prompt_builder import prepare_prompt
from solver.solver import Solver

ASSISTANT_CONTENT = """
You need to decide if the input from user is todo task or it has
any kind information about date and is a calendar event.

###

USER: 'Przypomnij mi, że mam kupić mleko'
AI: {"tool":"ToDo","desc":"Kup mleko" }

USER: 'Jutro mam spotkanie z Marianem'
AI: {"tool":"Calendar","desc":"Spotkanie z Marianem","date":"2023-11-16"}'

### 
Today is 2023-11-15

"""
USER_CONTENT = "{information}"


def tools(input_data: dict) -> dict:
    information = input_data["question"]
    oai = OpenAIConnector()
    prompt = prepare_prompt(
        ASSISTANT_CONTENT, USER_CONTENT.format(information=information)
    )
    answer = oai.generate_answer(model=OpenAiModels.gpt4.value, messages=prompt)
    jsonify_answer = json.loads(answer)
    prepared_answer = {"answer": jsonify_answer}
    return prepared_answer


if __name__ == "__main__":
    sol = Solver("tools")
    sol.solve(tools)
