from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import Choice, DataflowHierarchy, Dataset, Question, QuestionGroup, Role, Survey, Topic


class CreatorAdminMixin:
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']

    def save_model(self, request, obj, form, change):
        if not change or not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


class CreatorAdmin(admin.ModelAdmin, CreatorAdminMixin):
    pass


@admin.register(DataflowHierarchy)
class DataflowHierarchyAdmin(DraggableMPTTAdmin, CreatorAdminMixin):
    list_display = ['tree_actions', 'indented_title', 'project']
    list_select_related = ['project']


@admin.register(Role)
class RoleAdmin(CreatorAdmin):
    list_display = ['name', 'hierarchy']
    list_filter = ['hierarchy__project']
    list_select_related = ['hierarchy']


@admin.register(Survey)
class SurveyAdmin(CreatorAdmin):
    search_fields = ['id', 'uuid', 'name', 'code']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
    list_display = ['name', 'research_question', 'is_active']
    list_filter = ['is_active', 'created_at']
    autocomplete_fields = ['creator', 'project']
    prepopulated_fields = {'code': ['name']}


@admin.register(Topic)
class TopicAdmin(CreatorAdmin):
    list_display = ['name', 'survey']
    list_select_related = ['survey']
    list_filter = ['survey__project']


@admin.register(Dataset)
class DatasetAdmin(CreatorAdmin):
    list_display = ['name', 'topic']
    list_select_related = ['topic']


@admin.register(QuestionGroup)
class QuestionGroupAdmin(CreatorAdmin):
    list_display = ['name', 'survey']
    list_display_link = ['name', 'survey']
    list_select_related = ['survey']


class ChoiceInline(admin.TabularInline):
    model = Choice


@admin.register(Question)
class QuestionAdmin(CreatorAdmin):
    list_display = ['label', 'name', 'survey']
    list_select_related = ['survey']
    list_filter = ['name', 'survey__project']
    inlines = [ChoiceInline]
