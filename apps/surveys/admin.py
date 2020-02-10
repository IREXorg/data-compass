from django.contrib import admin

from .models import Survey


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    search_fields = ['id', 'uuid', 'name', 'code']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
    list_display = ['name', 'learning_enquiry', 'is_active']
    list_filter = ['is_active', 'created_at']
    autocomplete_fields = ['creator', 'project']
    prepopulated_fields = {'code': ['name']}

    def save_model(self, request, obj, form, change):
        if not change or not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
