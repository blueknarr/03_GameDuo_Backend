import pytz

from bossraid.models import RaidsHistory


def get_user_raid_history(user_id):
    res = []
    total_score = 0

    records = RaidsHistory.objects.filter(user_id=user_id).all()

    for record in records:
        total_score += record.score
        res.append({
            'raidRecordId': record.raids_id,
            'score': record.score,
            'enterTime': record.enter_time.astimezone(tz=pytz.timezone('Asia/Seoul')),
            'endTime': record.end_time.astimezone(tz=pytz.timezone('Asia/Seoul'))
        })

    return res, total_score
