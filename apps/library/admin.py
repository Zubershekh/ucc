from django.contrib import admin
from .models import LegalDocument
from apps.core.models import StatusTaxonomy


@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'document_number', 
        'title_en', 
        'document_type', 
        'publication_date', 
        'effective_date', 
        'status', 
        'is_featured'
    )
    list_filter = ('document_type', 'status', 'language', 'publication_date')
    search_fields = ('title_en', 'title_gu', 'document_number', 'summary_en', 'summary_gu')
    prepopulated_fields = {'slug': ('title_en',)}
    autocomplete_fields = ('superseded_by',)
    
    fieldsets = (
        ("Primary Identification & Gazette Metadata", {
            "fields": (
                ("title_en", "title_gu"),
                "slug",
                ("document_type", "document_number"),
                ("issuing_authority_en", "issuing_authority_gu"),
                "jurisdiction",
            )
        }),
        ("Dates & Strict Operational Status", {
            "fields": (
                ("publication_date", "effective_date"),
                "status",
                "superseded_by",
            )
        }),
        ("Official Provenance & File Verification", {
            "fields": (
                "official_source_url",
                ("file", "file_size_formatted"),
                "file_checksum",
                "relevant_sections",
                "language",
            )
        }),
        ("Neutral Plain-Language Summaries", {
            "fields": (
                "summary_en",
                "summary_gu",
            )
        }),
        ("Editorial Verification & Notes", {
            "fields": (
                ("verified_by", "is_featured"),
                "editorial_notes",
            )
        }),
    )

    actions = ['mark_in_force', 'mark_commencement_notified']

    @admin.action(description="Mark selected documents as: Commencement Notified")
    def mark_commencement_notified(self, request, queryset):
        queryset.update(status=StatusTaxonomy.COMMENCEMENT_NOTIFIED)

    @admin.action(description="Mark selected documents as: In Force")
    def mark_in_force(self, request, queryset):
        queryset.update(status=StatusTaxonomy.IN_FORCE)
