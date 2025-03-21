from core.cache.redis_manager import get_redis_template
from config import settings

redis_template = None
if settings.ENABLE_REDIS:
    redis_template = get_redis_template()

__all__ = ['redis_template']