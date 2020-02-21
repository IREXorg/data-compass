from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import (Choice, DataflowHierarchy, Dataset, DatasetAccess, DatasetFrequency, DatasetResponse,
                     DatasetStorage, DatasetTopicReceived, DatasetTopicResponse, DatasetTopicShared,
                     DatasetTopicStorageAccess, Entity, Question, QuestionGroup, QuestionResponse, Respondent, Response,
                     Role, Survey, Topic)


class CreatorAdminMixin:
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']

    def save_model(self, request, obj, form, change):
        if not change or not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


class CreatorAdmin(CreatorAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Survey)
class SurveyAdmin(CreatorAdmin):
    search_fields = ['id', 'uuid', 'name', 'code']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
    list_display = ['pk', 'name', 'research_question', 'is_active']
    list_filter = ['is_active', 'created_at']
    autocomplete_fields = ['creator', 'project']
    prepopulated_fields = {'code': ['name']}


@admin.register(DataflowHierarchy)
class DataflowHierarchyAdmin(CreatorAdminMixin, DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'level_name', 'project', 'pk']
    list_select_related = ['project']


@admin.register(Role)
class RoleAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'hierarchy']
    list_filter = ['hierarchy__project']
    list_select_related = ['hierarchy']


@admin.register(Entity)
class EntityAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'hierarchy']
    list_filter = ['hierarchy__project']
    list_select_related = ['hierarchy']


@admin.register(Topic)
class TopicAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'survey']
    list_select_related = ['survey']
    list_filter = ['survey__project']


@admin.register(Dataset)
class DatasetAdmin(CreatorAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


@admin.register(DatasetStorage)
class DatasetStorageAdmin(CreatorAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


@admin.register(DatasetAccess)
class DatasetAccessAdmin(CreatorAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


@admin.register(DatasetFrequency)
class DatasetFrequencyAdmin(CreatorAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']


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


@admin.register(QuestionGroup)
class QuestionGroupAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'survey']
    list_display_links = ['name', 'survey']
    list_select_related = ['survey']


class ChoiceInline(admin.TabularInline):
    model = Choice


@admin.register(Question)
class QuestionAdmin(CreatorAdmin):
    list_display = ['pk', 'label', 'name', 'survey']
    list_select_related = ['survey']
    list_filter = ['name', 'survey__project']
    inlines = [ChoiceInline]


@admin.register(Respondent)
class RespondentAdmin(CreatorAdmin):
    list_display = ['pk', 'email', 'first_name', 'last_name', 'survey', 'gender']
    list_display_links = ['pk', 'email']
    list_select_related = ['survey', 'gender']
    list_filter = ['gender', 'survey__project']
    autocomplete_fields = ['survey', 'creator', 'user']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']


class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse


@admin.register(Response)
class ResponseAdmin(CreatorAdmin):
    list_display = ['pk', 'respondent', 'survey']
    list_display_links = ['pk', 'respondent']
    list_select_related = ['survey', 'respondent']
    list_filter = ['survey__project', 'created_at']
    autocomplete_fields = ['survey']
    raw_id_fields = ['respondent']
    inlines = [QuestionResponseInline]


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
    list_select_related = ['response__respondent', 'dataset', 'survey']
    list_filter = ['response__survey__project']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'respondent', 'question', 'data']
    list_display_links = ['pk', 'respondent']
    list_select_related = ['response__respondent', 'question']
    list_filter = ['response__survey__project']
    raw_id_fields = ['question']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
