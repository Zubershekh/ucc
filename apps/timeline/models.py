from django.db import models
from apps.core.models import StatusTaxonomy
from apps.library.models import LegalDocument


class TimelineCategory(models.TextChoices):
    ASSEMBLY = "ASSEMBLY", "Legislative Assembly Proceedings / વિધાનસભા કાર્યવાહી"
    ASSENT = "ASSENT", "Presidential Assent / રાષ્ટ્રપતિ મંજૂરી"
    GAZETTE = "GAZETTE", "Official Gazette Publication / સત્તાવાર ગેઝેટ પ્રકાશન"
    COMMITTEE = "COMMITTEE", "High-Level Committee Report / સમિતિ અહેવાલ"
    RULES = "RULES", "Rules Formulation & Notifications / નિયમોની રચના"
    COMMENCEMENT = "COMMENCEMENT", "Commencement / કાયદાનો અમલ"


class TimelineEvent(models.Model):
    """
    Chronological record of Gujarat UCC milestones tracking legislative history,
    assent, gazette, and implementation status with verified source links.
    """
    title_en = models.CharField(max_length=255)
    title_gu = models.CharField(max_length=255)
    event_date = models.DateField(help_text="Exact date event transpired.")
    
    category = models.CharField(
        max_length=30, 
        choices=TimelineCategory.choices, 
        default=TimelineCategory.GAZETTE
    )
    status_label = models.CharField(
        max_length=50, 
        choices=StatusTaxonomy.CHOICES, 
        default=StatusTaxonomy.PUBLISHED_IN_GAZETTE
    )
    
    description_en = models.TextField()
    description_gu = models.TextField()
    
    official_source_title = models.CharField(
        max_length=255, 
        default="Official Gazette / Government Release"
    )
    official_source_url = models.URLField()
    related_document = models.ForeignKey(
        LegalDocument, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="timeline_events"
    )
    
    is_verified = models.BooleanField(
        default=True, 
        help_text="Flag indicating provenance has been confirmed against primary legal records."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-event_date', '-id']
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"

    def __str__(self):
        return f"{self.event_date.strftime('%d %b %Y')} - {self.title_en}"
