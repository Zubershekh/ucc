from django.db import models
from django.urls import reverse


class Topic(models.Model):
    """The 6 Core Subject Areas of Gujarat UCC 2026."""
    name_en = models.CharField(max_length=200, help_text="e.g., Marriage & Registration")
    name_gu = models.CharField(max_length=200, help_text="e.g., લગ્ન અને નોંધણી")
    slug = models.SlugField(max_length=200, unique=True)
    summary_en = models.TextField(help_text="Concise plain-language overview of the topic.")
    summary_gu = models.TextField(help_text="ગુજરાતીમાં વિષયનો સંક્ષિપ્ત સારાંશ.")
    overview_body_en = models.TextField(blank=True, help_text="Detailed overview of UCC provisions for this topic.")
    overview_body_gu = models.TextField(blank=True, help_text="વિગતવાર જોગવાઈઓની સમજૂતી.")
    icon_name = models.CharField(max_length=50, default="scale", help_text="Icon identifier (e.g., ring, scale, tree, file, heart, shield)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    meta_title_en = models.CharField(max_length=200, blank=True)
    meta_title_gu = models.CharField(max_length=200, blank=True)
    meta_desc_en = models.CharField(max_length=300, blank=True)
    meta_desc_gu = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['order', 'name_en']
        verbose_name = "UCC Topic"
        verbose_name_plural = "UCC Topics"

    def __str__(self):
        return f"{self.name_en} ({self.name_gu})"

    def get_absolute_url(self):
        return reverse('topic_detail', kwargs={'slug': self.slug})
