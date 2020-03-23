from django.contrib import admin

from core.mixins import CreatorAdminMixin

from .models import Respondent


@admin.register(Respondent)
class RespondentAdmin(CreatorAdminMixin, admin.ModelAdmin):
    list_display = ['pk', 'email', 'first_name', 'last_name', 'survey', 'gender']
    list_display_links = ['pk', 'email']
    list_select_related = ['survey', 'gender']
    list_filter = ['gender', 'survey__project']
    autocomplete_fields = ['survey', 'creator', 'user']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
