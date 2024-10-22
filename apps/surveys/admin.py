from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import (Choice, DataflowHierarchy, Dataset, DatasetAccess, DatasetFrequency, DatasetStorage, Entity,
                     HierarchyLevel, Question, QuestionGroup, Role, Survey, Topic)


class CreatorAdminMixin:
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


class CreatorAdmin(CreatorAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Survey)
class SurveyAdmin(CreatorAdmin):
    search_fields = ['id', 'uuid', 'name', 'code']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
    list_display = ['pk', 'name', 'research_question', 'is_active']
    list_display_links = ['pk', 'name']
    list_filter = ['is_active', 'created_at']
    autocomplete_fields = ['creator', 'project']
    prepopulated_fields = {'code': ['name']}
    filter_horizontal = ['genders']


@admin.register(HierarchyLevel)
class HierarchyLevelAdmin(CreatorAdminMixin, DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'project', 'pk']
    list_select_related = ['project']


@admin.register(DataflowHierarchy)
class DataflowHierarchyAdmin(CreatorAdminMixin, DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'level_name', 'project', 'pk']
    list_select_related = ['project']


@admin.register(Role)
class RoleAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'hierarchy_level', 'survey']
    list_display_links = ['pk', 'name']
    list_filter = ['hierarchy_level__project', 'survey']
    list_select_related = ['hierarchy_level', 'survey']


@admin.register(Entity)
class EntityAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'hierarchy_level', 'survey']
    list_display_links = ['pk', 'name']
    list_select_related = ['hierarchy_level', 'survey']
    list_filter = ['survey__project', 'survey']


@admin.register(Topic)
class TopicAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'survey']
    list_select_related = ['survey']
    list_filter = ['survey__project']


@admin.register(Dataset)
class DatasetAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'survey']
    list_display_links = ['pk', 'name']
    list_select_related = ['survey']


@admin.register(DatasetStorage)
class DatasetStorageAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'survey']
    list_display_links = ['pk', 'name']
    list_select_related = ['survey']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']


@admin.register(DatasetAccess)
class DatasetAccessAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'survey']
    list_display_links = ['pk', 'name']
    list_select_related = ['survey']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']


@admin.register(DatasetFrequency)
class DatasetFrequencyAdmin(CreatorAdmin):
    list_display = ['pk', 'name', 'survey']
    list_display_links = ['pk', 'name']
    list_select_related = ['survey']
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
