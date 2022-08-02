from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, user_name, password, **other_fields):
        user = self.model(user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(user_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(_('User Name'), max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'

    objects = UserManager()

    def __str__(self):
        return f'Id: {self.id}, User Name: {self.user_name}'

    class Meta:
        db_table='tb_users'