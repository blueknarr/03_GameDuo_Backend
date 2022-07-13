from django.db import models
from user.models import User


# Create your models here.
class RaidsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raids_id = models.BigIntegerField('Boss Raids Id')
    level = models.IntegerField('Level')
    score = models.IntegerField('Score')
    enter_time = models.DateTimeField('Enter Time')
    end_time = models.DateTimeField('End Time')

    class Meta:
        db_table = 'tb_raids_history'

    def __str__(self):
        return f'Id: {self.id}, BossRaids ID: {self.raids_id}, Level: {self.level}, Score: {self.score}'