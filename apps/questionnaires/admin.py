from django.contrib import admin

from .models import Questionnaire


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    search_fields = ['id', 'uuid', 'name', 'phase']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
    list_display = ['name', 'description', 'phase']
    list_filter = ['phase']
    autocomplete_fields = ['project', 'organization']

    def save_model(self, request, obj, form, change):
        if not change or not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
