from django.contrib import admin
from .models import SiteSettings, AuditLog


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name_en', 'current_status', 'last_verified_date', 'show_announcement')
    fieldsets = (
        ("Platform Brand & Status", {
            "fields": (
                ("site_name_en", "site_name_gu"),
                "current_status",
                ("status_summary_en", "status_summary_gu"),
                "last_verified_date",
            )
        }),
        ("Official Repositories & Committee Links", {
            "fields": (
                "verified_official_source_url",
                "official_committee_url",
            )
        }),
        ("Announcement Banner", {
            "fields": (
                "show_announcement",
                ("announcement_banner_en", "announcement_banner_gu"),
            )
        }),
        ("Mandatory Legal Disclaimers", {
            "fields": (
                "mandatory_disclaimer_en",
                "mandatory_disclaimer_gu",
            )
        }),
    )

    def has_add_permission(self, request):
        # Enforce singleton
        return not SiteSettings.objects.exists()


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model_name', 'object_repr', 'ip_address')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'object_repr', 'notes')
    readonly_fields = ('timestamp', 'user', 'action', 'model_name', 'object_id', 'object_repr', 'ip_address', 'notes')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
