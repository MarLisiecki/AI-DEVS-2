import os
import re
import tempfile

import requests
from typing import List

from open_ai_connector.open_ai_connector import OpenAIConnector
from solver.solver import Solver


def extract_url(string_with_url: str) -> str:
    # Regular expression to match URLs
    url_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    return url_pattern.findall(string_with_url)[0]


def whisper(input_data: dict):
    url_with_mp3 = extract_url(input_data["msg"])
    response = requests.get(url_with_mp3)
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".mp3", dir=tempfile.gettempdir()
    ) as temp_file:
        temp_file.write(response.content)
        audio_file = open(
            os.path.join(tempfile.gettempdir(), os.path.basename(temp_file.name)), "rb"
        )
        oai = OpenAIConnector()
        transcript = oai.use_whisperer(audio_file)
        prepared_answer = {"answer": transcript}
        return prepared_answer


if __name__ == "__main__":
    sol = Solver("whisper")
    sol.solve(whisper)
