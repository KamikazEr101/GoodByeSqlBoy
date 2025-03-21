from functools import lru_cache

from autogen_agentchat.conditions import TextMessageTermination,MaxMessageTermination

# 自定义termination, 默认规则是 超过设置的最大上下文消息数量 或者 在conclusion_agent结束发言 触发
@lru_cache(maxsize=1)
def get_termination(source: str, max_messages: int):
    return TextMessageTermination(source=source) | MaxMessageTermination(max_messages=max_messages)