import uuid

from django.db import models
from user.models import User


# Create your models here.
class RaidsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raids_id = models.UUIDField('Boss Raids Id', default=uuid.uuid4, editable=False)
    level = models.IntegerField('Level')
    score = models.IntegerField('Score')
    enter_time = models.DateTimeField('Enter Time')
    end_time = models.DateTimeField('End Time', auto_now=True)

    class Meta:
        db_table = 'tb_raids_history'

    def __str__(self):
        return f'Id: {self.id}, BossRaids ID: {self.raids_id}, Level: {self.level}, Score: {self.score}'


class RaidsTotalScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)

    class Meta:
        db_table= 'tb_total_score'

    def __str__(self):
        return f'Id: {self.id}, Total Score: {self.total_score}'