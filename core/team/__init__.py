from core.team.RRGC_team import get_team
from core.team.Selector_team import get_team_selector
from config import settings

sql_generator_team = get_team()

if settings.ENABLE_SELECTOR_TEAM:
    sql_generator_team = get_team_selector()

__all__ = [sql_generator_team]