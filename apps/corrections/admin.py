from django.contrib import admin
from django.utils import timezone
from .models import CorrectionReport, CorrectionStatus


@admin.register(CorrectionReport)
class CorrectionReportAdmin(admin.ModelAdmin):
    list_display = (
        'reference_page_or_topic', 
        'correction_type', 
        'status', 
        'submitter_name', 
        'created_at', 
        'assigned_editor'
    )
    list_filter = ('status', 'correction_type', 'created_at')
    search_fields = (
        'reference_page_or_topic', 
        'specific_error_description', 
        'suggested_correction', 
        'official_source_proof'
    )
    readonly_fields = ('created_at',)

    fieldsets = (
        ("Public Report Submission", {
            "fields": (
                "reference_page_or_topic",
                "correction_type",
                "specific_error_description",
                "suggested_correction",
                "official_source_proof",
                ("submitter_name", "submitter_email"),
                "created_at",
            )
        }),
        ("Editorial Triage & Resolution Log", {
            "fields": (
                "status",
                "assigned_editor",
                "internal_review_notes",
                "public_resolution_note",
                "resolved_at",
            )
        }),
    )

    actions = ['mark_investigating', 'mark_resolved']

    @admin.action(description="Triage: Move to Under Investigation")
    def mark_investigating(self, request, queryset):
        queryset.update(status=CorrectionStatus.INVESTIGATING)

    @admin.action(description="Triage: Mark Resolved (Resolution note must be filled)")
    def mark_resolved(self, request, queryset):
        queryset.update(status=CorrectionStatus.RESOLVED, resolved_at=timezone.now())
