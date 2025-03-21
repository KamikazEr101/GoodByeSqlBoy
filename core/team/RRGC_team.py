from numba.cuda.cudadrv.devicearray import lru_cache

from core.agents import sql_generator_agent, critic_agent, optimize_agent, conclusion_agent
from config import settings
from core.termination import termination

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

participant_agent=[sql_generator_agent]

if settings.ENABLE_CRITIC_AGENT:
    participant_agent.append(critic_agent)
if settings.ENABLE_OPTIMIZE_AGENT:
    participant_agent.append(optimize_agent)

participant_agent.append(conclusion_agent)

@lru_cache
def get_rrgc_team():
    return RoundRobinGroupChat(
        participants=participant_agent,
        termination_condition=termination,
    )

if __name__ == '__main__':
    import asyncio
    async def main():
        await Console(
            get_rrgc_team().run_stream(task='查询id为1的员工的所有信息(id, 姓名, 年龄, 地址, 邮箱), 这本次对话中你可以省略表的结构当做单表查询')
        )
    asyncio.run(main())