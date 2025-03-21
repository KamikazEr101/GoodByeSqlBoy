from core.termination.generate_termination import get_termination
from config import settings

termination = get_termination(source='conclusion_agent')

__all__ = ["termination"]