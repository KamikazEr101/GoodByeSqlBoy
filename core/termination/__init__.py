from core.termination.generate_termination import get_termination
from config import settings

termination = get_termination(source='conclusion_agent', max_messages=settings.MAX_CONTEXT_MESSAGES)

__all__ = ["termination"]