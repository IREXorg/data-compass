from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as CoreUserAdmin

from .models import Gender, User


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'code')
    list_display_link = ('pk', 'name')
    readonly_fields = ('id', 'uuid', 'created_at', 'modified_at')
    prepopulated_fields = {'code': ('name',)}


@admin.register(User)
class UserAdmin(CoreUserAdmin):
    fieldsets = CoreUserAdmin.fieldsets

    # add custom personal info
    fieldsets[1][1]['fields'] += ('phone_number', 'gender', 'country', 'address', 'avatar')

    # add custom permission flags
    fieldsets[2][1]['fields'] += ('is_respondent', 'is_facilitator')

    list_filter = CoreUserAdmin.list_filter + ('gender', )
