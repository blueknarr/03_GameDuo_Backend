import uuid

from django.shortcuts import render
from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.response import Response


class RaidStartApi(APIView):
    def set_raid(self, request, raid_status, can_entered):
        raid_status['userId'] = request.data['user_id']
        raid_status['level'] = request.data['level']
        raid_status['raidRecordId'] = str(uuid.uuid4())
        raid_status['isEntered'] = can_entered
        raid_status['lastEnterTime'] = datetime.now()
        cache.set('status', raid_status)

        return can_entered

    def post(self, request):
        raid_status = cache.get('status')
        can_entered = True

        diff = datetime.now() - raid_status['lastEnterTime']

        """
        1. isEnterd -> False, 보스레이드 입장 가능
        2. 같은 유저가 이전 보스레이드를 끝낸 시간이 180초 이상 되었으면 입장 가능
        """
        if not raid_status['isEntered']:
            can_entered = self.set_raid(request, raid_status, can_entered)
        elif raid_status['userId'] == request.data['user_id'] and diff.seconds > 180:
            can_entered = self.set_raid(request, raid_status, can_entered)
        else:
            can_entered = False

        return Response({
            'isEntered': can_entered,
            'raidRecordId': raid_status['raidRecordId']
        }, status=status.HTTP_200_OK)