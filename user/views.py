from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import UserSerializer, UserModelSerializer

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
            user = User.objects.filter(id=user_id)

            return Response({
                'users': UserModelSerializer(user[0]).data,
                'totalScore': user[0].total_score
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
            id = User.objects.filter(user_name=serializer.validated_data['user_name']).values('id')[0]['id']

            return Response({
                'userId': id
            }, status=status.HTTP_201_CREATED)