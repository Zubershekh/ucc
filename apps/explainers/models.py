from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from apps.core.models import StatusTaxonomy, EditorialStatus
from apps.topics.models import Topic
from apps.library.models import LegalDocument


class Explainer(models.Model):
    """
    Plain-Language Legal Explainer adhering to editorial standards,
    source citations, reviewer attribution, and last-verified tracking.
    """
    title_en = models.CharField(max_length=300)
    title_gu = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="explainers")
    
    summary_deck_en = models.TextField(help_text="Editorial deck/summary explaining practical impact.")
    summary_deck_gu = models.TextField(help_text="વ્યવહારિક અસરો દર્શાવતો ગુજરાતી પરિચય.")
    
    # Core Editorial Breakdown
    what_the_text_says_en = models.TextField(help_text="Plain-language explanation of what statutory text says.")
    what_the_text_says_gu = models.TextField(help_text="કાયદાની મૂળ કલમો શું કહે છે તેનું સરળ ગુજરાતી વિશ્લેષણ.")
    
    who_is_covered_en = models.TextField(help_text="Jurisdiction, applicability, and individuals covered.")
    who_is_covered_gu = models.TextField(help_text="કોના પર અને કઈ પરિસ્થિતિમાં લાગુ પડે છે?")
    
    exceptions_en = models.TextField(help_text="Statutory exceptions, exempt communities, or conditions.")
    exceptions_gu = models.TextField(help_text="અપવાદો, મુક્તિ અને વિશેષ શરતો.")
    
    procedural_steps_en = models.TextField(blank=True, help_text="Procedures/steps (Only when rules are verified).")
    procedural_steps_gu = models.TextField(blank=True, help_text="પ્રક્રિયાના તબક્કા (માત્ર જ્યારે નિયમો જાહેર થયેલ હોય).")
    
    misconceptions_en = models.TextField(blank=True, help_text="Common rumors vs legal statutory facts.")
    misconceptions_gu = models.TextField(blank=True, help_text="સામાન્ય ગેરમાન્યતાઓ સામે કાયદાકીય સત્ય.")

    # Status & Legal Provenance
    legal_status_badge = models.CharField(
        max_length=50, 
        choices=StatusTaxonomy.CHOICES, 
        default=StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        help_text="Current legal operational status of provisions described in this explainer."
    )
    editorial_status = models.CharField(
        max_length=30, 
        choices=EditorialStatus.CHOICES, 
        default=EditorialStatus.PUBLISHED
    )
    
    primary_document = models.ForeignKey(
        LegalDocument, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="explainers",
        help_text="Primary statutory document cited."
    )
    source_citations = models.TextField(
        help_text="Exact Section and clause citations (e.g. Sections 8, 9, 14 of Gujarat Act 17 of 2026)."
    )
    
    # Attributions & Verification Dates
    author_name = models.CharField(max_length=150, default="Gujarat UCC Legal Editorial Desk")
    legal_reviewer_name = models.CharField(
        max_length=150, 
        default="Adv. H. S. Trivedi, High Court of Gujarat (Legal QA)",
        help_text="Qualified advocate or legal scholar who reviewed this substantive explainer."
    )
    last_verified_date = models.DateField(help_text="Last date official sources were verified.")
    reviewed_date = models.DateField(null=True, blank=True)
    next_review_date = models.DateField(null=True, blank=True)
    
    correction_history = models.TextField(
        blank=True, 
        help_text="Log of corrections, updates, or clarification additions made to this explainer."
    )
    
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_verified_date', '-created_at']
        verbose_name = "Legal Explainer Guide"
        verbose_name_plural = "Legal Explainer Guides"

    def __str__(self):
        return f"{self.title_en} [{self.topic.name_en}]"

    def get_absolute_url(self):
        return reverse('explainer_detail', kwargs={'slug': self.slug})
