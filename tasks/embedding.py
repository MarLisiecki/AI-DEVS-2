from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.solver import Solver


def embedding(to_embedded: str):
    oai = OpenAIConnector()
    embedding = oai.generate_embedding(to_embedded)
    prepared_answer = {"answer": embedding}
    return prepared_answer


if __name__ == "__main__":
    text_for_embedding = "Hawaiian pizza"
    sol = Solver("embedding")
    sol.solve(embedding, additional_data=text_for_embedding)
