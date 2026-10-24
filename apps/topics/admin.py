from django.contrib import admin
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('order', 'name_en', 'name_gu', 'slug', 'is_active')
    list_display_links = ('name_en', 'name_gu')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name_en',)}
    search_fields = ('name_en', 'name_gu', 'summary_en', 'summary_gu')
    fieldsets = (
        ("Subject Nomenclature", {
            "fields": (
                ("name_en", "name_gu"),
                "slug",
                "icon_name",
                ("order", "is_active")
            )
        }),
        ("Summaries & Statutory Overview", {
            "fields": (
                ("summary_en", "summary_gu"),
                ("overview_body_en", "overview_body_gu"),
            )
        }),
        ("SEO Metadata", {
            "classes": ("collapse",),
            "fields": (
                ("meta_title_en", "meta_title_gu"),
                ("meta_desc_en", "meta_desc_gu"),
            )
        }),
    )
