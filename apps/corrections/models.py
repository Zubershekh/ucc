from django.db import models
from django.contrib.auth.models import User


class CorrectionType(models.TextChoices):
    FACTUAL_ERROR = "FACTUAL_ERROR", "Factual Inaccuracy in Explanation / વિશ્લેષણમાં ભૂલ"
    DATE_MISMATCH = "DATE_MISMATCH", "Date or Milestone Discrepancy / તારીખ અથવા સમયરેખાની વિસંગતતા"
    STATUTORY_CITATION = "STATUTORY_CITATION", "Incorrect Section Citation / કલમ સંદર્ભમાં ક્ષતિ"
    BROKEN_LINK = "BROKEN_LINK", "Broken Official Source Link / તૂટેલી લિંક"
    TRANSLATION_ISSUE = "TRANSLATION_ISSUE", "Translation Inaccuracy / ભાષાંતરમાં ભૂલ"
    NEW_SOURCE = "NEW_SOURCE", "New Official Notification Published / નવું સત્તાવાર જાહેરનામું ઉપલબ્ધ"


class CorrectionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending Triage / પ્રાથમિક ચકાસણી પેન્ડિંગ"
    INVESTIGATING = "INVESTIGATING", "Under Legal Review / કાનૂની સમીક્ષા હેઠળ"
    RESOLVED = "RESOLVED", "Resolved & Content Updated / ઉકેલાયેલ અને સામગ્રી સુધારી"
    REJECTED = "REJECTED", "Verified Accurate (No Correction Needed) / ચકાસાયેલ સચોટ (સુધારો અનાવશ્યક)"


class CorrectionReport(models.Model):
    """
    Public correction submission queue adhering to Section 6 and Section 11 guardrails:
    Explicit privacy safeguards, no sensitive case files or personal documents.
    """
    reference_page_or_topic = models.CharField(
        max_length=255, 
        help_text="URL, Explainer Title, or Document cited."
    )
    correction_type = models.CharField(
        max_length=40, 
        choices=CorrectionType.choices, 
        default=CorrectionType.FACTUAL_ERROR
    )
    
    specific_error_description = models.TextField(
        help_text="Clear explanation of the error or discrepancy identified."
    )
    suggested_correction = models.TextField(
        help_text="What the correct text or citation should be."
    )
    official_source_proof = models.TextField(
        help_text="Link, Gazette number, or verifiable official reference supporting this correction."
    )
    
    # Optional Submitter Info (Privacy Safeguard: No sensitive Aadhaar/Case files allowed)
    submitter_name = models.CharField(max_length=150, blank=True)
    submitter_email = models.EmailField(blank=True)
    
    status = models.CharField(
        max_length=30, 
        choices=CorrectionStatus.choices, 
        default=CorrectionStatus.PENDING
    )
    
    assigned_editor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="assigned_corrections"
    )
    internal_review_notes = models.TextField(blank=True, help_text="Internal notes during verification.")
    public_resolution_note = models.TextField(
        blank=True, 
        help_text="Public correction notice text added to article correction history upon resolution."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Correction / Feedback Report"
        verbose_name_plural = "Corrections Triage Queue"

    def __str__(self):
        return f"[{self.get_status_display()}] {self.reference_page_or_topic} ({self.get_correction_type_display()})"
