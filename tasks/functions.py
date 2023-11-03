from open_ai_connector.const import OpenAiModels
from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.prompt_builder import prepare_prompt
from solver.solver import Solver


ASSISTANT_CONTENT = ""
USER_CONTENT = "I would like to add user Adam Smith that was born in 1986"


FUNCTIONS = [
    {
        "name": "addUser",
        "description": "Add user to stdout",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the user",
                },
                "surname": {
                    "type": "string",
                    "description": "Surname of the user",
                },
                "year": {
                    "type": "integer",
                    "description": "Year of born",
                },
            },
            "required": ["name", "surname", "year"],
        },
    }
]


def addUser(name: str, surname: str, year: int) -> None:
    print(f"I'm adding user {name}, {surname}, that was born in {year}")


def functions(input_data: dict):
    oai = OpenAIConnector()
    prompt = prepare_prompt(
        ASSISTANT_CONTENT,
        USER_CONTENT,
    )
    name_of_the_function, arguments = oai.function_calls(
        model=OpenAiModels.gpt4.value, messages=prompt, functions=FUNCTIONS
    )
    func_to_call = eval(name_of_the_function)
    func_to_call(**arguments)
    prepared_answer = {"answer": FUNCTIONS[0]}
    return prepared_answer


if __name__ == "__main__":
    sol = Solver("functions")
    sol.solve(functions)
