from config import token
from openai import OpenAI
from db.MySqlConn import config

OPENAI_CHAT_COMPLETION_OPTIONS = {
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stream": True,
    # "stop": None,
    "model": config["AI"]["MODEL"]
}

async def ChatCompletionsAI(logged_in_user, messages, multimodal: bool) -> (str, str):
    level = logged_in_user.get("level")
    openAIConfig = {'api_key': config["AI"]["TOKEN"]}

    if multimodal:
        OPENAI_CHAT_COMPLETION_OPTIONS["model"] = config["AI"]["MULTIMODAL"]
    else:
        OPENAI_CHAT_COMPLETION_OPTIONS["model"] = config["AI"]["MODEL"]

    answer = ""
    client = OpenAI(**openAIConfig)
    with client.chat.completions.with_streaming_response.create(
            messages=messages,
            max_tokens=token[level],
            **OPENAI_CHAT_COMPLETION_OPTIONS) as response:
        for r in response.parse():
            if r.choices:
                delta = r.choices[0].delta
                if delta.content:
                    answer += delta.content
                yield answer, r.choices[0].finish_reason