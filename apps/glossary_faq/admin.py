from django.contrib import admin
from .models import FAQ, GlossaryTerm


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('order', 'question_en', 'topic', 'is_published', 'is_featured', 'legal_reviewer')
    list_display_links = ('question_en',)
    list_editable = ('order', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'topic')
    search_fields = ('question_en', 'question_gu', 'short_answer_en', 'short_answer_gu', 'citations')
    autocomplete_fields = ('topic',)
    fieldsets = (
        ("Question & Topical Subject", {
            "fields": (
                ("question_en", "question_gu"),
                ("topic", "order"),
                ("is_published", "is_featured"),
            )
        }),
        ("Short Answer & In-depth Legal Rationale", {
            "fields": (
                ("short_answer_en", "short_answer_gu"),
                ("detailed_answer_en", "detailed_answer_gu"),
            )
        }),
        ("Statutory Citations & Verification", {
            "fields": (
                "citations",
                "legal_reviewer",
            )
        }),
    )


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ('term_en', 'term_gu', 'statutory_source', 'order')
    list_editable = ('order',)
    search_fields = ('term_en', 'term_gu', 'plain_language_definition_en', 'plain_language_definition_gu')
    fieldsets = (
        ("Term Equivalents", {
            "fields": (
                ("term_en", "term_gu"),
                ("statutory_source", "order"),
            )
        }),
        ("Plain-Language Definitions", {
            "fields": (
                ("plain_language_definition_en", "plain_language_definition_gu"),
            )
        }),
        ("Verbatim Statutory Definitions", {
            "fields": (
                ("statutory_definition_en", "statutory_definition_gu"),
                "related_terms",
            )
        }),
    )
