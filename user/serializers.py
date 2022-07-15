from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_name'
        ]


class UserSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=30, write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_user_name(self, user_name):
        if not user_name:
            raise ValueError(_('유저 이름을 넣어주세요'))

        get_user_name = User.objects.filter(user_name__iexact=user_name)

        if get_user_name.count() > 0:
            raise ValueError(
                _('이미 등록한 유저 이름입니다.')
            )
        return user_name

    def validate(self, data):
        data['user_name'] = self.validate_user_name(data['user_name'])
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            user_name=validated_data['user_name'],
            password=validated_data['password']
        )
        return user
