from core.agents.agents import *

sql_generator_agent = get_sql_generator_agent()
critic_agent = get_critic_agent()
optimize_agent = get_optimize_agent()
conclusion_agent = get_conclusion_agent()

__all__ = [sql_generator_agent, critic_agent, optimize_agent,conclusion_agent]