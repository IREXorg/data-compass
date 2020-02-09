from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['id', 'uuid', 'name', 'code']
    readonly_fields = ['id', 'uuid', 'created_at', 'modified_at']
    list_display = ['name', 'country', 'description']
    list_filter = ['country']
    autocomplete_fields = ['creator', 'members']

    def save_model(self, request, obj, form, change):
        if not change or not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
