import os
from typing import List

import openai
from dotenv import load_dotenv

from open_ai_connector.const import OpenAiModels


class OpenAIConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OpenAIConnector, cls).__new__(cls, *args, **kwargs)
            cls._instance.set_api_key()
        return cls._instance

    def set_api_key(self) -> None:
        if os.getenv("OPENAI_API_KEY") is None:
            load_dotenv()
            openai.api_key = os.getenv("OPENAI_API_KEY")
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_models(self) -> List[str]:
        models = openai.Model.list()
        models_name = [model["id"] for model in models["data"]]
        return models_name

    def moderate_prompt(self, sentences: List[str]) -> List[str]:
        verdicts = []
        for sentence in sentences:
            response = openai.Moderation.create(input=sentence)
            verdict = response.results[0].flagged
            verdicts.append(verdict)
        return verdicts

    def generate_answer(
        self,
        model: str,
        messages: List[dict],
        max_token: int = 150,
        variations: int = 1,
        temperature: float = 0.5,
    ) -> str:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            max_tokens=max_token,
            n=variations,
            messages=messages,
        )
        return response.choices[0].message.content

    def generate_embedding(self, text_to_embbeded: str) -> str:
        embedding = openai.Embedding.create(
            input=text_to_embbeded, model=OpenAiModels.text_embedding_ada_002.value
        )["data"][0]["embedding"]
        return embedding


if __name__ == "__main__":
    pass
