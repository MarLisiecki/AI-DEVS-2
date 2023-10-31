from solver.solver import Solver


def hello_api(input_data: dict) -> dict:
    processed_data = input_data["cookie"]
    prepared_answer = {"answer": processed_data}
    return prepared_answer


if __name__ == "__main__":
    sol = Solver("helloapi")
    sol.solve(hello_api)
