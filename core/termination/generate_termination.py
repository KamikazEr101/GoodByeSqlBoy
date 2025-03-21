from functools import lru_cache

from autogen_agentchat.conditions import TextMessageTermination

@lru_cache(maxsize=1)
def get_termination(source: str):
    return TextMessageTermination(source=source)