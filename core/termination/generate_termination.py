from functools import lru_cache

from autogen_agentchat.conditions import TextMessageTermination,MaxMessageTermination

@lru_cache(maxsize=1)
def get_termination(source: str, max_messages: int):
    return TextMessageTermination(source=source) | MaxMessageTermination(max_messages=max_messages)