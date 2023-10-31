import copy
from typing import List, Optional

from solver.const import BASE_PROMPT


def prepare_prompt(
    assistant_content: str, user_content: str, system_content: Optional[str] = None
) -> List[dict]:
    prompt = copy.deepcopy(BASE_PROMPT)
    for role in prompt:
        if role["role"] == "system":
            if system_content:
                role["content"] = system_content
            else:
                continue
        elif role["role"] == "user":
            role["content"] = user_content
        elif role["role"] == "assistant":
            role["content"] = assistant_content
    if system_content is None:
        prompt.pop(0)
    return prompt
