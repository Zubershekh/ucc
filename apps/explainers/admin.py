from django.contrib import admin
from .models import Explainer
from apps.core.models import EditorialStatus


@admin.register(Explainer)
class ExplainerAdmin(admin.ModelAdmin):
    list_display = (
        'title_en', 
        'topic', 
        'editorial_status', 
        'legal_status_badge', 
        'legal_reviewer_name', 
        'last_verified_date', 
        'is_featured', 
        'views_count'
    )
    list_filter = ('editorial_status', 'legal_status_badge', 'topic', 'last_verified_date')
    search_fields = ('title_en', 'title_gu', 'summary_deck_en', 'summary_deck_gu', 'source_citations')
    prepopulated_fields = {'slug': ('title_en',)}
    autocomplete_fields = ('topic', 'primary_document')

    fieldsets = (
        ("Explainer Title & Subject Pillar", {
            "fields": (
                ("title_en", "title_gu"),
                "slug",
                ("topic", "is_featured"),
                ("summary_deck_en", "summary_deck_gu"),
            )
        }),
        ("Section Breakdown (Plain-Language vs Statutory Text)", {
            "fields": (
                ("what_the_text_says_en", "what_the_text_says_gu"),
                ("who_is_covered_en", "who_is_covered_gu"),
                ("exceptions_en", "exceptions_gu"),
                ("procedural_steps_en", "procedural_steps_gu"),
                ("misconceptions_en", "misconceptions_gu"),
            )
        }),
        ("Legal Provenance & Statutory Citations", {
            "fields": (
                "legal_status_badge",
                "primary_document",
                "source_citations",
            )
        }),
        ("Reviewer Attribution & Verification Dates", {
            "fields": (
                ("author_name", "legal_reviewer_name"),
                ("last_verified_date", "reviewed_date", "next_review_date"),
            )
        }),
        ("Editorial Workflow Status & Errata Log", {
            "fields": (
                "editorial_status",
                "correction_history",
            )
        }),
    )

    actions = [
        'submit_for_legal_review', 
        'approve_and_publish', 
        'mark_needs_update', 
        'archive_explainer'
    ]

    @admin.action(description="Workflow: Submit for Legal Review")
    def submit_for_legal_review(self, request, queryset):
        queryset.update(editorial_status=EditorialStatus.LEGAL_REVIEW)

    @admin.action(description="Workflow: Legal Review Approved -> Publish")
    def approve_and_publish(self, request, queryset):
        queryset.update(editorial_status=EditorialStatus.PUBLISHED)

    @admin.action(description="Workflow: Flag as Needs Update (New Notification Available)")
    def mark_needs_update(self, request, queryset):
        queryset.update(editorial_status=EditorialStatus.NEEDS_UPDATE)

    @admin.action(description="Workflow: Archive Explainer")
    def archive_explainer(self, request, queryset):
        queryset.update(editorial_status=EditorialStatus.ARCHIVED)
