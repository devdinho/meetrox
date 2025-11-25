from django.contrib import admin
from crm_integration.models import PreSignUp


@admin.register(PreSignUp)
class PreSignUpAdmin(admin.ModelAdmin):
    list_display = ('email', 'origin', 'created_at')
    search_fields = ('email', 'origin__name')
    list_filter = ('origin', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('origin',)