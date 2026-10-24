from django.db import models
from apps.topics.models import Topic


class FAQ(models.Model):
    """
    Searchable question-and-answer entries linked to detailed guides
    and primary legal sources.
    """
    question_en = models.CharField(max_length=300)
    question_gu = models.CharField(max_length=300)
    
    short_answer_en = models.TextField(help_text="One-paragraph quick answer.")
    short_answer_gu = models.TextField(help_text="એક ફકરામાં સીધો જવાબ.")
    
    detailed_answer_en = models.TextField(help_text="In-depth legal context, citations, and caveats.")
    detailed_answer_gu = models.TextField(help_text="વિગતવાર કાનૂની સંદર્ભ અને જોગવાઈઓ.")
    
    topic = models.ForeignKey(
        Topic, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="faqs"
    )
    citations = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="e.g. Sections 5 & 6, Gujarat Act 17 of 2026"
    )
    legal_reviewer = models.CharField(
        max_length=150, 
        blank=True, 
        default="Adv. H. S. Trivedi, High Court of Gujarat"
    )
    
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "FAQ Entry"
        verbose_name_plural = "Frequently Asked Questions (FAQs)"

    def __str__(self):
        return f"{self.question_en} ({self.question_gu})"


class GlossaryTerm(models.Model):
    """
    Plain-language definitions of statutory terms with statutory citations
    and language equivalents (Gujarati & English).
    """
    term_en = models.CharField(max_length=150)
    term_gu = models.CharField(max_length=150)
    
    plain_language_definition_en = models.TextField(help_text="Simple layman explanation in English.")
    plain_language_definition_gu = models.TextField(help_text="સામાન્ય નાગરિક સમજી શકે તેવી ગુજરાતી વ્યાખ્યા.")
    
    statutory_definition_en = models.TextField(blank=True, help_text="Verbatim definition from statute.")
    statutory_definition_gu = models.TextField(blank=True, help_text="કાયદામાંથી શબ્દશઃ વ્યાખ્યા.")
    
    statutory_source = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="e.g. Section 2(c), Gujarat Act 17 of 2026"
    )
    related_terms = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Related terms separated by commas"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['term_en']
        verbose_name = "Glossary Term"
        verbose_name_plural = "Legal Glossary Terms"

    def __str__(self):
        return f"{self.term_en} / {self.term_gu}"
