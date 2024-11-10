from .prompts import Prompts

message = [
    {
        "role": "system",
        "content": Prompts.request_prompt
    },
    {
        "role": "user",
    },
]