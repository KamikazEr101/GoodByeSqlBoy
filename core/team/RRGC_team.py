from functools import lru_cache

from autogen_agentchat.ui import Console

from core.utils import hash_utils
from core.cache import redis_template
from core.agents import agent_list
from config import settings
from core.termination import termination
from core.cache import redis_template

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult

# RoundRobinGroupChatTeam
class SQLGenerateRRGCTeam:
    def __init__(self):
        self.core_team = RoundRobinGroupChat(
                            participants=agent_list,
                            termination_condition=termination,
                        )

    async def generate_sql(self, natural_language: str) -> str:
        await self.core_team.reset()
        # async for msg in self.core_team.run_stream(task=natural_language):
        #     if isinstance(msg, TaskResult):
        #         target_sql = msg.messages[-1].content
        result = await Console(
            self.core_team.run_stream(task=natural_language),
            output_stats=True,
        )
        target_sql = result.messages[-1].content
        self.__save_in_redis(natural_language, target_sql)
        return target_sql

    def __save_in_redis(self, k: str, v: str) -> None:
        if settings.ENABLE_REDIS:
            redis_template.set(hash_utils.sha256_encrypt(k), v, ex=settings.REDIS_TTL)

@lru_cache
def get_team():
    return SQLGenerateRRGCTeam()

