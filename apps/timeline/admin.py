from django.contrib import admin
from .models import TimelineEvent


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('event_date', 'title_en', 'category', 'status_label', 'is_verified')
    list_filter = ('category', 'status_label', 'is_verified', 'event_date')
    search_fields = ('title_en', 'title_gu', 'description_en', 'description_gu', 'official_source_title')
    autocomplete_fields = ('related_document',)
    fieldsets = (
        ("Milestone Event Details", {
            "fields": (
                ("title_en", "title_gu"),
                ("event_date", "category"),
                "status_label",
                ("description_en", "description_gu"),
            )
        }),
        ("Official Source Provenance", {
            "fields": (
                ("official_source_title", "official_source_url"),
                "related_document",
                "is_verified",
            )
        }),
    )
