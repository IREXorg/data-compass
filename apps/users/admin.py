from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as CoreUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(CoreUserAdmin):
    fieldsets = CoreUserAdmin.fieldsets

    # add custom personal info
    fieldsets[1][1]['fields'] += ('phone_number', 'country', 'address', 'avatar')

    # add custom permission flags
    fieldsets[2][1]['fields'] += ('is_respondent', 'is_facilitator')
