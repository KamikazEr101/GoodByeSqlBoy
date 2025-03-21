from core.agents.agents import *
from config import settings

agent_list = [get_sql_generator_agent()]

if settings.ENABLE_CRITIC_AGENT:
    agent_list.append(get_critic_agent())
if settings.ENABLE_OPTIMIZE_AGENT:
    agent_list.append(get_optimize_agent())

agent_list.append(get_conclusion_agent())

__all__ = [agent_list]