from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class UserAdminConfig(UserAdmin):
    ordering = ('-user_name',)
    list_display = ('user_name', 'total_score', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('user_name', 'total_score')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'total_score', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )


admin.site.register(User, UserAdminConfig)