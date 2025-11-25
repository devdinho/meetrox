from django.contrib import admin
from crm_integration.models import Crm_Integration


@admin.register(Crm_Integration)
class CrmIntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'url')
    list_filter = ('is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
