from django.db import models
from django.urls import reverse
from apps.core.models import StatusTaxonomy


class DocumentType(models.TextChoices):
    ACT = "ACT", "Enacted Act / વિધેયક-કાયદો"
    GAZETTE = "GAZETTE", "Official Extraordinary Gazette / અસાધારણ ગેઝેટ"
    NOTIFICATION = "NOTIFICATION", "Government Notification / સરકારી જાહેરનામું"
    RULES = "RULES", "Subordinate Rules & Regulations / નિયમો અને વિનિયમો"
    FORMS = "FORMS", "Prescribed Statutory Form / નિયત વૈધાનિક ફોર્મ"
    CIRCULAR = "CIRCULAR", "Administrative Circular / વહીવટી પરિપત્ર"
    COMMITTEE = "COMMITTEE", "UCC Committee Report / કમિટી અહેવાલ"
    JUDICIAL = "JUDICIAL", "Relevant Judicial Reference / સંબંધિત ન્યાયિક ચુકાદો"


class LegalDocument(models.Model):
    """
    Official primary source legal documents adhering strictly to Section 5 requirements:
    title, document type, issuing authority, jurisdiction, document number,
    dates, status, official URL, file checksum/version, relevant sections, summary, superseded-by.
    """
    title_en = models.CharField(max_length=300)
    title_gu = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    
    document_type = models.CharField(
        max_length=30, 
        choices=DocumentType.choices, 
        default=DocumentType.GAZETTE
    )
    issuing_authority_en = models.CharField(max_length=200, default="Government of Gujarat")
    issuing_authority_gu = models.CharField(max_length=200, default="ગુજરાત સરકાર / વિધાન સભા")
    jurisdiction = models.CharField(max_length=150, default="Gujarat, India")
    
    document_number = models.CharField(
        max_length=150, 
        help_text="e.g. Gujarat Act No. 17 of 2026 / Extraordinary Gazette Vol. LXVII"
    )
    publication_date = models.DateField(help_text="Date printed or published in Gazette.")
    effective_date = models.DateField(
        null=True, 
        blank=True, 
        help_text="Date appointed for commencement. LEAVE BLANK if not yet appointed by Gazette notification."
    )
    
    status = models.CharField(
        max_length=50, 
        choices=StatusTaxonomy.CHOICES, 
        default=StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        help_text="Strict legal status. Never infer 'In force' without a verified commencement notification."
    )
    
    official_source_url = models.URLField(
        help_text="Direct link to official government repository (e.g. NeVA, uccgujarat.in, or egazette)."
    )
    file = models.FileField(upload_to="documents/%Y/%m/", blank=True, null=True)
    file_checksum = models.CharField(max_length=100, blank=True, help_text="SHA-256 checksum for legal provenance.")
    file_size_formatted = models.CharField(max_length=30, default="1.8 MB", help_text="e.g., 2.4 MB PDF")
    
    relevant_sections = models.CharField(max_length=255, blank=True, help_text="e.g., Sections 1-45, Schedule I")
    language = models.CharField(
        max_length=20, 
        choices=[('gu', 'Gujarati (ગુજરાતી)'), ('en', 'English'), ('both', 'Bilingual (ગુજરાતી / English)')],
        default='both'
    )
    
    summary_en = models.TextField(help_text="Neutral, plain-language description of document contents.")
    summary_gu = models.TextField(help_text="દસ્તાવેજના વિષયવસ્તુનો તટસ્થ અને સ્પષ્ટ ગુજરાતી સારાંશ.")
    
    superseded_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='supersedes',
        help_text="If this document was amended or superseded by a newer notification."
    )
    
    access_date = models.DateField(auto_now_add=True)
    verified_by = models.CharField(max_length=150, blank=True, default="Editorial Legal QA Team")
    editorial_notes = models.TextField(blank=True, help_text="Internal notes regarding legal provenance.")
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-publication_date', 'title_en']
        verbose_name = "Legal Document"
        verbose_name_plural = "Legal Document Library"

    def __str__(self):
        return f"[{self.get_document_type_display()}] {self.title_en} ({self.document_number})"

    def get_absolute_url(self):
        return reverse('document_detail', kwargs={'slug': self.slug})
