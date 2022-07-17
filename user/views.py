from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from bossraid.models import RaidsHistory
from user.serializers import UserSerializer
from user.utils.utils import get_user_raid_history

User = get_user_model()


class UserApi(APIView):
    serializer_class = UserSerializer

    def get(self, request, user_id):
        """
        유저 정보 조회
        :param user_id: Int
        :return: Json
        """
        try:
            records, total_score = get_user_raid_history(user_id)

            return Response({
                'totalScore': total_score,
                'bossRaidHistory': records
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'users': '유저 정보가 없습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        유저 생성
        :param request: String
        :return: Int
        """
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.filter(user_name=serializer.validated_data['user_name']).first()

            return Response({
                'userId': user.id
            }, status=status.HTTP_201_CREATED)