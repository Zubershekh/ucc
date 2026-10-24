from django.db import models
from django.urls import reverse
from apps.core.models import EditorialStatus
from apps.timeline.models import TimelineEvent


class NewsCategory(models.TextChoices):
    OFFICIAL_UPDATE = "OFFICIAL_UPDATE", "Official Legal Update / સત્તાવાર કાનૂની અપડેટ"
    FACT_CHECK = "FACT_CHECK", "Legal Fact-Check / કાનૂની સત્ય-તપાસ (Fact Check)"
    EXPLAINER_BRIEF = "EXPLAINER_BRIEF", "Editorial Brief / સંપાદકીય સંક્ષિપ્ત"
    PRESS_STATEMENT = "PRESS_STATEMENT", "Official Statement / સરકારી નિવેદન"


class FactCheckStatus(models.TextChoices):
    OFFICIAL_CONFIRMED = "OFFICIAL_CONFIRMED", "Verified by Primary Legal Source / સત્તાવાર સ્ત્રોતથી ચકાસાયેલ"
    IN_PROCESS = "IN_PROCESS", "Verification In Process / ચકાસણી પ્રક્રિયા હેઠળ"
    MEDIA_REPORT = "MEDIA_REPORT", "Media Reporting (Awaiting Gazette) / મીડિયા અહેવાલ (ગેઝેટ પેન્ડિંગ)"
    MISLEADING_DEBUNKED = "MISLEADING_DEBUNKED", "Misleading Claim Debunked / ગેરમાર્ગે દોરતી બાબતનું ખંડન"


class NewsArticle(models.Model):
    """
    Editorial news reporting, legislative notifications, fact checks,
    and official progress reports with transparent sourcing.
    """
    headline_en = models.CharField(max_length=300)
    headline_gu = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    
    category = models.CharField(
        max_length=40, 
        choices=NewsCategory.choices, 
        default=NewsCategory.OFFICIAL_UPDATE
    )
    fact_check_status = models.CharField(
        max_length=40, 
        choices=FactCheckStatus.choices, 
        default=FactCheckStatus.OFFICIAL_CONFIRMED
    )
    
    excerpt_en = models.TextField(help_text="Short lead summary for homepage news feed.")
    excerpt_gu = models.TextField(help_text="મુખ્ય સમાચાર ફીડ માટે સંક્ષિપ્ત સારાંશ.")
    
    body_en = models.TextField()
    body_gu = models.TextField()
    
    author_name = models.CharField(max_length=150, default="Legislative Affairs Desk")
    reviewer_name = models.CharField(max_length=150, blank=True, default="Editorial Board")
    
    sources_list = models.TextField(
        help_text="List of official sources, gazette issues, or verified reports consulted."
    )
    
    related_timeline_event = models.ForeignKey(
        TimelineEvent, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="articles"
    )
    
    editorial_status = models.CharField(
        max_length=30, 
        choices=EditorialStatus.CHOICES, 
        default=EditorialStatus.PUBLISHED
    )
    
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags (e.g. Gazette, Assembly, Marriage)")
    is_breaking = models.BooleanField(default=False)
    published_date = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "News & Update Article"
        verbose_name_plural = "News & Updates Articles"

    def __str__(self):
        return f"[{self.get_category_display()}] {self.headline_en}"

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})
