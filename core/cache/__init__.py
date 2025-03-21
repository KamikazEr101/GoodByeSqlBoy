from core.cache.redis_manager import get_redis_template

redis_template = get_redis_template()

__all__ = ['redis_template']