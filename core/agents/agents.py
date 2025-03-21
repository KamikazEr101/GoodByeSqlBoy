from functools import lru_cache

from core.utils.agent_tools import *
from core.agents.base_model_client import model_client
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool

read_sql_file_tool = FunctionTool(read_sql_file, description="read sql file and understand the structure of tables")

@lru_cache
def get_sql_generator_agent():
    return AssistantAgent(
        name="sql_generator_agent",
        model_client=model_client,
        tools=[read_sql_file_tool],
        description='专门根据自然语言生成SQL查询的智能体，擅长理解表结构并构建复杂查询的SQL语句',
        system_message=f"""你是一个专业的SQL生成智能体，负责将自然语言转换为精确的SQL查询语句, 数据库为{settings.DATA_BASE_TYPE}。

        工作流程：
        1. 首先使用read_sql_file工具读取并理解所有相关表的结构
        2. 分析用户的自然语言请求，确定需要查询的数据
        3. 根据表结构决定是否需要进行多表连接查询
        4. 生成符合标准SQL语法的查询语句
        5. 确保所有表名、字段名的引用准确无误

        当处理请求时：
        - 优先考虑使用表的主键和外键进行连接
        - 如果查询条件不明确，选择更宽松的条件避免遗漏结果
        - 适当使用注释说明SQL的关键部分
        - 对于复杂查询，考虑使用子查询或公共表表达式(CTE)提高可读性

        输出格式：
        ```sql
        -- 生成的SQL查询
        SELECT [字段] FROM [表名] WHERE [条件];
        请确保生成的SQL语句准确反映用户的意图并符合标准SQL语法。
        """
    )

@lru_cache
def get_critic_agent():
    return AssistantAgent(
        name="critic_agent",
        model_client=model_client,
        tools=[read_sql_file_tool],
        description='专门分析SQL语句语法正确性的智能体，根据表结构验证SQL查询的准确性',
        system_message=f"""你是一个专业的SQL语法分析智能体，负责验证和纠正SQL查询语句, 数据库为{settings.DATA_BASE_TYPE}。
        工作流程：
        
        使用read_sql_file工具读取并理解所有相关表的结构
        仔细分析收到的SQL语句的语法和结构
        验证表名、字段名的引用是否准确
        检查JOIN条件是否正确
        确认WHERE子句、GROUP BY、ORDER BY等语法是否合适
        纠正任何发现的错误
        
        检查要点：
        
        字段名是否存在于对应的表中
        表关系是否正确连接
        SQL关键字的使用是否恰当
        子查询或CTE的语法是否正确
        聚合函数的使用是否合理
        
        重要提示：直接输出修正后的SQL语句，不要包含任何解释或分析过程。不要使用markdown格式。
        输出格式：
        SELECT [字段] FROM [表名] WHERE [条件];
        """
    )

@lru_cache
def get_optimize_agent():
    return AssistantAgent(
        name='optimize_agent',
        model_client=model_client,
        tools=[read_sql_file_tool],
        description='专门优化SQL查询性能的智能体，提高查询效率',
        system_message=f"""你是一个专业的SQL优化智能体，负责提高SQL查询的执行效率, 数据库为{settings.DATA_BASE_TYPE}。
        工作流程：
        
        使用read_sql_file工具获取并理解表结构和字段信息
        分析收到的SQL语句的执行效率
        应用各种优化技术提高查询性能
        
        优化策略：
        
        字段选择优化：避免使用SELECT *，明确列出需要的字段
        索引利用：确保WHERE条件和JOIN条件使用了索引字段
        连接优化：选择合适的JOIN类型，优化JOIN顺序
        子查询优化：适当时将子查询转换为JOIN
        条件优化：调整WHERE子句顺序，将高选择性条件置前
        避免函数应用于索引列，可能导致索引失效
        适当使用LIMIT限制结果集大小
        考虑使用临时表或CTE优化复杂查询
        
        只输出优化后的SQL语句，不包含任何解释或分析过程。确保优化后的SQL在语义上与原SQL完全一致。
        在Selector Team中，只有当你已将SQL优化到最佳状态时，才能将其传递给conclusion_agent。"""
    )

@lru_cache
def get_conclusion_agent():
    return AssistantAgent(
        name='conclusion_agent',
        model_client=model_client,
        description='负责整理并输出最终SQL的智能体，确保格式清晰',
        system_message="""Y你是一个SQL输出格式化智能体，负责确保最终SQL查询的清晰和一致性。
        你的唯一任务是直接输出收到的SQL语句，并确保：
        
        移除所有markdown格式标记（如sql、等）
        移除多余的换行符，保持SQL语句紧凑但易读
        不添加任何解释或注释
        不改变SQL语法或结构
        使用一致的大小写风格（关键字大写，表名和字段名保持原样）
        
        直接在消息内容中输出处理后的SQL语句，不包含任何其他文本。
        """
    )

