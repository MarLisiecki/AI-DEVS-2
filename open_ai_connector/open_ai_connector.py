import json
import os
from typing import List, BinaryIO, Tuple

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

    def function_calls(
        self,
        model: str,
        messages: List[dict],
        functions: List[dict],
        function_call: str = "auto",
        max_token: int = 150,
        variations: int = 1,
        temperature: float = 0.5,
    ) -> Tuple[str, dict]:
        response = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            max_tokens=max_token,
            n=variations,
            messages=messages,
            functions=functions,
            function_call=function_call,
        )
        # === Return in structure [name_of_the_function, arguments]
        reply_content = response.choices[0].message.to_dict()
        return (
            reply_content["function_call"]["name"],
            json.loads(reply_content["function_call"]["arguments"]),
        )

    def generate_embedding(self, text_to_embbeded: str) -> str:
        embedding = openai.Embedding.create(
            input=text_to_embbeded, model=OpenAiModels.text_embedding_ada_002.value
        )["data"][0]["embedding"]
        return embedding

    def use_whisperer(self, audio_file: BinaryIO) -> str:
        transcript = openai.Audio.transcribe(
            model=OpenAiModels.whisper_1.value, file=audio_file, response_format="text"
        )
        return transcript

    def use_vision(self, text, url, assistant_knowledge):
        response = (
            openai.ChatCompletion.create(
                model=OpenAiModels.gpt4_vision.value,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": url,
                                },
                            },
                        ],
                    },
                    {"role": "assistant", "content": assistant_knowledge},
                ],
                max_tokens=300,
            ),
        )

        print(response[0]["choices"][0]["message"]["content"])
        return response[0]["choices"][0]["message"]["content"]


if __name__ == "__main__":
    pass
