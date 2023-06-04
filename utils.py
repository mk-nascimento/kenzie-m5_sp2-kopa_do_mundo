import math
from datetime import datetime as dt

from exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError


def data_processing(soccer_time_info: dict):
    current_year: int = dt.now().year
    first_world_cup: int = 1930
    # math_float_cups: float | int = (current_year - first_world_cup) / 4
    # cups_into_now: int = math.floor(math_float_cups)

    # %Y Year with century as a decimal number.
    # %m Month as a zero-padded decimal number.
    # %d Day of the month as a zero-padded decimal number.
    DATE_FORMAT: str = "%Y-%m-%d"

    if soccer_time_info["titles"] < 0:
        raise NegativeTitlesError()

    soccer_time_first_cup: str = soccer_time_info["first_cup"]
    soccer_time_first_cup_year: int = dt.strptime(
        soccer_time_first_cup, DATE_FORMAT
    ).year
    years_after_first_world_cup: int = soccer_time_first_cup_year - first_world_cup
    years_after_first_participation = current_year - soccer_time_first_cup_year

    if years_after_first_world_cup % 4 or soccer_time_first_cup_year < first_world_cup:
        raise InvalidYearCupError()

    cups_after_first_participation: int = math.floor(
        years_after_first_participation / 4
    )

    if cups_after_first_participation < soccer_time_info["titles"]:
        raise ImpossibleTitlesError()
