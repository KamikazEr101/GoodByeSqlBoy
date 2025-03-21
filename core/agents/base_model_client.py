from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
from config import settings

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=settings.OPENAI_API_KEY,
)

