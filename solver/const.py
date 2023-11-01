BASE_AUTH_URL = "https://zadania.aidevs.pl/token/{task}"
BASE_TASK_URL = "https://zadania.aidevs.pl/task/{token}"
BASE_ANSWER_URL = "https://zadania.aidevs.pl/answer/{token}"

BASE_PROMPT = [
    {"role": "system", "content": "{system_content}"},
    {"role": "user", "content": "{user_content}"},
    {"role": "assistant", "content": "{assistant_content}"},
]
