import datetime
import pytz

from django.core.cache import cache, caches

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


def get_level_score(level):
    data = cache.get('bossRaids')['bossRaids'][0]['levels']

    for row in data:
        if row['level'] == level:
            return row['score']


def redis_get_client():
    return caches['default'].client.get_client()


def get_raid_top_ranker(key):
    top_ranker = redis_get_client().zrevrange(key, start=0, end=5, withscores=True)

    res = []
    for idx, ranker in enumerate(top_ranker):
        res.append({
            'Ranking': idx,
            'User Id': ranker[0],
            'Total Score': int(ranker[1])
        })
    return res


def get_my_ranking_info(key, user_id):
    redis_client = redis_get_client()
    my_ranking = {
        'Ranking': redis_client.zrevrank(key, user_id),
        'User Id': user_id,
        'Total Score': int(redis_client.zscore(key, user_id))
    }
    return my_ranking


def set_raid_score(key, user_id, score):
    redis_client = redis_get_client()

    if not redis_client.zscore(key, user_id):
        redis_client.zadd(key, {user_id: score})
    else:
        redis_client.zincrby(key, score, user_id)
