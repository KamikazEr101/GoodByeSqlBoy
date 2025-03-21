from numba.cuda.cudadrv.devicearray import lru_cache

from core.agents.base_model_client import model_client
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

@lru_cache
def get_sql_generator_agent():
    return AssistantAgent(
        name="sql_generator_agent",
        model_client=model_client,
        description='An agent that generate SQL through natural language using the context of the structure of tables',
        system_message="""You are an SQL generator agent that generates SQL queries through natural language.
        You should using the context of the structure of tables to generate SQL queries.
        """
    )

@lru_cache
def get_critic_agent():
    return AssistantAgent(
        name="natural_language_analysis_agent",
        model_client=model_client,
        description='An agent that analyzes SQL statements and combines the structure of tables to determine whether the SQL syntax is correct',
        system_message="""You are an SQL syntax analysis agent. 
        You need to analysis the SQL statements using the structure of tables.
        You don't need to point out the reason why the SQL is wrong.
        You just need output the final correct SQL with no natural language.
        """
    )

@lru_cache
def get_optimize_agent():
    return AssistantAgent(
        name='optimize_agent',
        model_client=model_client,
        description='An agent that optimizes SQL queries.',
        system_message="""You are an SQL optimization agent.
        You need to optimize the SQL queries using the structure of tables.
        You should optimize the SQLs' timecost by some ways but do not make the SQL syntax wrong.
        You just need output the final optimized SQL with no natural language.
        """
    )

@lru_cache
def get_conclusion_agent():
    return AssistantAgent(
        name='conclusion_agent',
        model_client=model_client,
        description='An agent that concludes SQL queries.',
        system_message="""You are an text analysis agent.
        You need to directly print the SQL in the message.
        You must not change the SQL syntax.
        You just need output the final SQL with no natural language directly in the message content.
        You need remove the markdown signals
        """
    )


