from django.contrib import admin

from .models import (DatasetResponse, DatasetTopicReceived, DatasetTopicResponse, DatasetTopicShared,
                     DatasetTopicStorageAccess, QuestionResponse, SurveyResponse)


class CreatorAdminMixin:
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


class CreatorAdmin(CreatorAdminMixin, admin.ModelAdmin):
    pass


@admin.register(SurveyResponse)
class SurveyResponseAdmin(CreatorAdmin):
    list_display = ['pk', 'respondent', 'survey']
    list_display_links = ['pk', 'respondent']
    list_select_related = ['survey', 'respondent']
    list_filter = ['survey__project', 'created_at']
    autocomplete_fields = ['survey']
    raw_id_fields = ['respondent']


@admin.register(DatasetResponse)
class DatasetResponseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'respondent', 'dataset', 'survey']
    list_display_links = ['pk', 'respondent']
    list_select_related = ['response__respondent', 'dataset', 'response__survey']
    list_filter = ['response__survey__project']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']


@admin.register(DatasetTopicResponse)
class DatasetTopicResponseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'respondent', 'dataset', 'topic', 'survey']
    list_display_links = ['pk', 'respondent']
    list_select_related = ['dataset_response__response__respondent', 'dataset_response__dataset',
                           'topic', 'dataset_response__response__survey']
    list_filter = ['dataset_response__response__survey__project']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'respondent', 'question', 'data']
    list_display_links = ['pk', 'respondent']
    list_select_related = ['response__respondent', 'question']
    list_filter = ['response__survey__project']
    raw_id_fields = ['question']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']


@admin.register(DatasetTopicReceived)
class DatasetTopicReceivedAdmin(admin.ModelAdmin):
    list_display = ['pk', 'entity', 'topic', 'dataset']
    list_display_links = ['pk', 'entity']
    list_select_related = ['entity', 'topic', 'dataset_response__dataset']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']


@admin.register(DatasetTopicShared)
class DatasetTopicSharedAdmin(admin.ModelAdmin):
    list_display = ['pk', 'entity', 'topic', 'dataset']
    list_display_links = ['pk', 'entity']
    list_select_related = ['entity', 'topic', 'dataset_response__dataset']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']


@admin.register(DatasetTopicStorageAccess)
class DatasetTopicStorageAccessAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
