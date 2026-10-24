from django.contrib import admin
from .models import NewsArticle
from apps.core.models import EditorialStatus


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = (
        'headline_en', 
        'category', 
        'fact_check_status', 
        'editorial_status', 
        'published_date', 
        'is_breaking'
    )
    list_filter = ('category', 'fact_check_status', 'editorial_status', 'is_breaking', 'published_date')
    search_fields = ('headline_en', 'headline_gu', 'excerpt_en', 'excerpt_gu', 'body_en', 'body_gu')
    prepopulated_fields = {'slug': ('headline_en',)}
    autocomplete_fields = ('related_timeline_event',)
    
    fieldsets = (
        ("Headline & Lead Summary", {
            "fields": (
                ("headline_en", "headline_gu"),
                "slug",
                ("category", "fact_check_status"),
                ("is_breaking", "editorial_status"),
                ("excerpt_en", "excerpt_gu"),
            )
        }),
        ("Article Body Content", {
            "fields": (
                ("body_en", "body_gu"),
            )
        }),
        ("Attribution & Sourcing", {
            "fields": (
                ("author_name", "reviewer_name"),
                "published_date",
                "sources_list",
                "related_timeline_event",
                "tags",
            )
        }),
    )

    actions = ['publish_news', 'mark_breaking']

    @admin.action(description="Publish selected articles")
    def publish_news(self, request, queryset):
        queryset.update(editorial_status=EditorialStatus.PUBLISHED)

    @admin.action(description="Toggle as Breaking Legal Update")
    def mark_breaking(self, request, queryset):
        queryset.update(is_breaking=True)
