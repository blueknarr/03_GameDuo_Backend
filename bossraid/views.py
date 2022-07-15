import uuid
import pytz

from django.shortcuts import render
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.response import Response
from bossraid.serializers import RaidsEndSerializer
from bossraid.utils.utils import get_diff_secs, get_limit_seconds


class RaidStartApi(APIView):
    def set_raid(self, request, raid_status, can_entered):
        """
        보스레이드 시작 시 상태 저장
        :param request: String
        :param raid_status: JSON
        :param can_entered: Bool
        :return: Bool
        """
        raid_status['userId'] = request.data['user_id']
        raid_status['level'] = int(request.data['level'])
        raid_status['raidRecordId'] = uuid.uuid4()
        raid_status['isEntered'] = can_entered
        raid_status['lastEnterTime'] = datetime.now().astimezone(tz=pytz.timezone('Asia/Seoul'))
        cache.set('status', raid_status)

        return can_entered

    def post(self, request):
        """
        보스레이드 시작
        :param request: String
        :return: JSON
        """
        raid_status = cache.get('status')
        can_entered = True

        """
        1. isEnterd -> False, 보스레이드 입장 가능
        2. 같은 유저가 이전 보스레이드를 끝낸 시간이 180초 이상 되었으면 입장 가능
        3. 유저가 보스레이드에 입장 중이라면 입장 불가
        """
        if not raid_status['isEntered']:
            can_entered = self.set_raid(request, raid_status, can_entered)
        elif raid_status['userId'] == request.data['user_id'] and get_diff_secs(datetime.now(), raid_status['lastEnterTime']) > get_limit_seconds():
            can_entered = self.set_raid(request, raid_status, can_entered)
        else:
            can_entered = False

        return Response({
            'isEntered': can_entered,
            'raidRecordId': raid_status['raidRecordId']
        }, status=status.HTTP_200_OK)


class RaidEndApi(APIView):
    serializer_class = RaidsEndSerializer

    def post(self, request):
        """
        보스레이드 종료
        :param request: String
        :return: JSON
        """
        user_id = request.data['user_id']
        raid_record_id = request.data['raids_id']
        flag = True
        raid_status = cache.get('status')

        """
        1. 현재 진행중인 보스레이드 상태와 종료를 요청한 userId, raidRecordId가 다르면 종료 불가
        2. 180초 이내에 게임을 마쳤다면, 보스레이드 기록 저장
        3. 180초를 초과했다면, 보스레이드 기록 저장 안함
        """
        if raid_status['userId'] != user_id and raid_status['raidRecordId'] != raid_record_id:
            flag = False
        else:
            if get_diff_secs(datetime.now(), raid_status['lastEnterTime']) <= get_limit_seconds():
                serializers = self.serializer_class(data=request.data)

                if serializers.is_valid(raise_exception=True):
                    serializers.save()
            else:
                raid_status['isEntered'] = False
                raid_status['raidRecordId'] = 0
                cache.set('status',raid_status)

        if flag:
            return Response({
                'message': f'보스레이스가 종료되었습니다. ({raid_record_id})'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'userId와 raidRecordId가 일치하지 않습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)