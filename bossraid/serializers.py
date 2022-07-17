from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.cache import cache
from bossraid.models import RaidsHistory
from django.utils.translation import gettext_lazy as _
from bossraid.utils.utils import get_level_score

User = get_user_model()


class RaidsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RaidsHistory
        fields = [
            'id',
            'raids_id',
            'level',
            'score',
            'enter_time',
            'end_time'
        ]


class RaidsEndSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(write_only=True)
    raids_id = serializers.UUIDField(write_only=True)

    def set_raid(self, raid_status):
        raid_status['raidRecordId'] = 0
        raid_status['isEntered'] = False
        cache.set('status', raid_status)
        return raid_status

    def validate_user(self, user_id):
        if not user_id:
            raise serializers.ValidationError(
                _('user_id field is not allowed empty')
            )
        return user_id

    def validate_raid_record_id(self, raid_record_id):
        if not raid_record_id:
            raise serializers.ValidationError(
                _('raid_record_id field is not allowed empty')
            )
        return raid_record_id

    def validate(self, data):
        data['user_id'] = self.validate_user(data['user_id'])
        data['raids_id'] = self.validate_raid_record_id(data['raids_id'])
        return data

    def create(self, validated_data):
        raid_status = cache.get('status')

        raids_history = RaidsHistory.objects.create(
            user_id=validated_data['user_id'],
            raids_id=validated_data['raids_id'],
            level=raid_status['level'],
            score=get_level_score(raid_status['level']),
            enter_time=raid_status['lastEnterTime']
        )
        self.set_raid(raid_status)
        return raids_history
