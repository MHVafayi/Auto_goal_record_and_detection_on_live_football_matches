from datetime import datetime, timedelta
from enum import Enum


class AskMe(Enum):
    WHEN_THE_MATCH_STARTS = 0
    BEFORE_THE_MATCH_STARTS = -1
    LATER = 1


def sumTwoTimes(time1: str, time2: str):
    dt1 = datetime.strptime(time1, '%Y%m%d%H%M')
    dt2 = datetime.strptime(time2, '%H%M')
    dt2_delta = timedelta(hours=dt2.hour, minutes=dt2.minute)
    dt3 = dt1 + dt2_delta
    return datetime.strftime(dt3, '%Y%m%d%H%M')


def minusTwoTimes(time1: str, time2: str):
    dt1 = datetime.strptime(time1, '%Y%m%d%H%M')
    dt2 = datetime.strptime(time2, '%H%M')
    dt2_delta = timedelta(hours=dt2.hour, minutes=dt2.minute)
    dt3 = dt1 - dt2_delta
    return datetime.strftime(dt3, '%Y%m%d%H%M')


