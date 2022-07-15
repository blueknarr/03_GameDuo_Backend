import datetime
import pytz

from django.core.cache import cache

RAIDS_STATUS={
    "userId": 0,
    "raidRecordId": 0,
    "isEntered": False,
    "lastEnterTime": datetime.datetime(2022, 1, 1, 0, 0, 0, 0, tzinfo=pytz.timezone('Asia/Seoul'))
}


def get_diff_secs(now_datetime, past_datetime):
    now_datetime = now_datetime.astimezone(tz=pytz.timezone('Asia/Seoul'))
    past_datetime = past_datetime.astimezone(tz=pytz.timezone('Asia/Seoul'))

    diff = now_datetime - past_datetime
    return diff.seconds


def get_limit_seconds():
    return cache.get('bossRaids')['bossRaids'][0]['bossRaidLimitSeconds']
