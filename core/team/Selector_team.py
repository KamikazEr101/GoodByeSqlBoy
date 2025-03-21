from functools import lru_cache
from typing import Sequence
from autogen_agentchat.ui import Console

from core.utils import hash_utils
from core.cache import redis_template
from core.agents import agent_list
from config import settings
from core.termination import termination
from core.cache import redis_template
from core.agents.base_model_client import model_client

from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.base import TaskResult

def custom_selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
    if messages[-1].source=='sql_generator_agent':
        return 'critic_agent'

    if messages[-1].source == 'critic_agent':
        if settings.ENABLE_OPTIMIZE_AGENT:
            return 'optimize_agent'
        else:
            return 'conclusion_agent'

    if settings.ENABLE_OPTIMIZE_AGENT:
        if len(messages)>3 and messages[-1].source=='optimize_agent' and messages[-2].source=='optimize_agent':
            return 'conclusion_agent'

    if messages[-1].source == 'optimize_agent':
        return 'optimize_agent'

    return None

class SelectorTeam:
    def __init__(self):
        self.selector_prompt="""You are a workflow coordinator for a team of SQL generation agents. Your job is to determine which agent should handle the current state of the conversation.
                
        The team consists of:
        1. sql_generator_agent: Generates initial SQL based on natural language and table structure
        2. natural_language_analysis_agent: Analyzes and validates the SQL syntax based on table structure
        3. optimize_agent: Optimizes the SQL for better performance
        4. conclusion_agent: Produces the final clean SQL output without markdown or other formatting
        
        Follow these rules to select the next agent:
        - Start with sql_generator_agent for new user requests
        - After sql_generator_agent produces SQL, select natural_language_analysis_agent to validate it
        - After natural_language_analysis_agent validates SQL, select optimize_agent for optimization
        - After optimize_agent optimizes SQL, select conclusion_agent to produce the final clean output
        - If the conversation flow is unclear, default to sql_generator_agent
        
        Based on the latest message and its content, select the most appropriate next agent.
        """
        self.core_team = SelectorGroupChat(
                            participants=agent_list,
                            model_client=model_client,
                            selector_prompt=self.selector_prompt,
                            termination_condition=termination,
                            allow_repeated_speaker=True,
                            selector_func=custom_selector_func,
                        )

    async def generate_sql(self, natural_language: str) -> str:
        # async for msg in self.core_team.run_stream(task=natural_language):
        #     if isinstance(msg, TaskResult):
        #         target_sql = msg.messages[-1].content
        #
        # self.__save_in_redis(natural_language, target_sql)
        result = await Console(
            self.core_team.run_stream(task=natural_language),
            output_stats=True,
        )
        return result.messages[-1].content

    def __save_in_redis(self, k: str, v: str) -> None:
        redis_template.set(hash_utils.sha256_encrypt(k), v, ex=settings.REDIS_TTL)

@lru_cache
def get_team_selector():
    return SelectorTeam()

