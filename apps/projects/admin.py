from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['id', 'uuid', 'name', 'code']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
    list_display = ['name', 'countries', 'description']
    autocomplete_fields = ['creator']

    def save_model(self, request, obj, form, change):
        if not change or not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
