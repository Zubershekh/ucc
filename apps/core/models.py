from django.db import models
from django.contrib.auth.models import User


class StatusTaxonomy:
    """Strict Status Taxonomy defined in Section 2 of Project Brief."""
    PASSED_BY_ASSEMBLY = "PASSED_BY_ASSEMBLY"
    PRESIDENTIAL_ASSENT = "PRESIDENTIAL_ASSENT"
    PUBLISHED_IN_GAZETTE = "PUBLISHED_IN_GAZETTE"
    COMMENCEMENT_NOTIFIED = "COMMENCEMENT_NOTIFIED"
    RULES_NOTIFIED = "RULES_NOTIFIED"
    IN_FORCE = "IN_FORCE"
    PROPOSED_REPORTED = "PROPOSED_REPORTED"
    UNDER_VERIFICATION = "UNDER_VERIFICATION"

    CHOICES = [
        (PASSED_BY_ASSEMBLY, "Passed by Assembly / વિધાનસભા દ્વારા પસાર"),
        (PRESIDENTIAL_ASSENT, "Presidential assent received / રાષ્ટ્રપતિની મંજૂરી પ્રાપ્ત"),
        (PUBLISHED_IN_GAZETTE, "Published in Gazette / ગેઝેટમાં પ્રકાશિત"),
        (COMMENCEMENT_NOTIFIED, "Commencement notified / અમલવારી જાહેર"),
        (RULES_NOTIFIED, "Rules notified / નિયમો અધિસૂચિત"),
        (IN_FORCE, "In force / કાયદો અમલમાં"),
        (PROPOSED_REPORTED, "Proposed / reported / પ્રસ્તાવિત અથવા અહેવાલિત"),
        (UNDER_VERIFICATION, "Under verification / ચકાસણી હેઠળ"),
    ]

    LABELS_EN = {
        PASSED_BY_ASSEMBLY: "Passed by Assembly",
        PRESIDENTIAL_ASSENT: "Presidential Assent Received",
        PUBLISHED_IN_GAZETTE: "Published in Gazette",
        COMMENCEMENT_NOTIFIED: "Commencement Notified",
        RULES_NOTIFIED: "Rules Notified",
        IN_FORCE: "In Force",
        PROPOSED_REPORTED: "Proposed / Reported",
        UNDER_VERIFICATION: "Under Verification",
    }

    LABELS_GU = {
        PASSED_BY_ASSEMBLY: "વિધાનસભા દ્વારા પસાર",
        PRESIDENTIAL_ASSENT: "રાષ્ટ્રપતિની મંજૂરી પ્રાપ્ત",
        PUBLISHED_IN_GAZETTE: "ગેઝેટમાં પ્રકાશિત",
        COMMENCEMENT_NOTIFIED: "અમલવારી જાહેરનામું",
        RULES_NOTIFIED: "નિયમો અધિસૂચિત",
        IN_FORCE: "કાયદો અમલમાં",
        PROPOSED_REPORTED: "પ્રસ્તાવિત / અહેવાલિત",
        UNDER_VERIFICATION: "ચકાસણી હેઠળ",
    }

    BADGE_CLASSES = {
        PASSED_BY_ASSEMBLY: "status-badge-neutral",
        PRESIDENTIAL_ASSENT: "status-badge-info",
        PUBLISHED_IN_GAZETTE: "status-badge-warning",
        COMMENCEMENT_NOTIFIED: "status-badge-success",
        RULES_NOTIFIED: "status-badge-success",
        IN_FORCE: "status-badge-success",
        PROPOSED_REPORTED: "status-badge-neutral",
        UNDER_VERIFICATION: "status-badge-alert",
    }


class EditorialStatus:
    """Editorial States defined in Section 5 of Project Brief."""
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    LEGAL_REVIEW = "LEGAL_REVIEW"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    PUBLISHED = "PUBLISHED"
    NEEDS_UPDATE = "NEEDS_UPDATE"
    ARCHIVED = "ARCHIVED"

    CHOICES = [
        (DRAFT, "Draft (ખરડો)"),
        (IN_REVIEW, "In Review (સંપાદકીય સમીક્ષા)"),
        (LEGAL_REVIEW, "Legal Review (કાનૂની સમીક્ષા)"),
        (APPROVED, "Approved (મંજૂર)"),
        (SCHEDULED, "Scheduled (શેડ્યૂલ કરેલ)"),
        (PUBLISHED, "Published (પ્રકાશિત)"),
        (NEEDS_UPDATE, "Needs Update (સુધારા જરૂરી)"),
        (ARCHIVED, "Archived (સંગ્રહિત)"),
    ]


class SiteSettings(models.Model):
    """Global platform configuration, state-wide verified legal status, and announcements."""
    site_name_en = models.CharField(max_length=200, default="Gujarat UCC Public Information Platform")
    site_name_gu = models.CharField(max_length=200, default="ગુજરાત સમાન નાગરિક સંહિતા (UCC) માહિતી મંચ")
    
    current_status = models.CharField(
        max_length=50, 
        choices=StatusTaxonomy.CHOICES, 
        default=StatusTaxonomy.PUBLISHED_IN_GAZETTE,
        help_text="Current state-wide verified legislative status of Gujarat UCC 2026."
    )
    status_summary_en = models.CharField(
        max_length=300,
        default="Presidential Assent received on 17 Sept 2026; Published in Extraordinary Gazette on 1 Oct 2026. Commencement notification by State Govt awaited."
    )
    status_summary_gu = models.CharField(
        max_length=300,
        default="૧૭ સપ્ટેમ્બર ૨૦૨૬ના રોજ રાષ્ટ્રપતિની મંજૂરી પ્રાપ્ત; ૧ ઓક્ટોબર ૨૦૨૬ના રોજ અસાધારણ ગેઝેટમાં પ્રકાશિત. રાજ્ય સરકાર દ્વારા અમલવારી જાહેરનામું બાકી છે."
    )

    last_verified_date = models.DateField(
        help_text="Date when official gazette and rules were last cross-checked."
    )
    verified_official_source_url = models.URLField(
        default="https://cms.neva.gov.in/NeVA/GJ/FileStructures/PaperLaid/15/8/AsIntroduced/17%20of2026_AsIn.pdf"
    )
    official_committee_url = models.URLField(default="https://uccgujarat.in/")
    
    announcement_banner_en = models.CharField(max_length=300, blank=True)
    announcement_banner_gu = models.CharField(max_length=300, blank=True)
    show_announcement = models.BooleanField(default=True)
    
    mandatory_disclaimer_en = models.TextField(
        default="Independent public informational platform. General legal information only; not legal advice. Consult a qualified advocate for individual circumstances. Not affiliated with any government entity."
    )
    mandatory_disclaimer_gu = models.TextField(
        default="સ્વતંત્ર જાહેર કાનૂની માહિતી મંચ. આ સામગ્રી માત્ર સામાન્ય માહિતી માટે છે, કાનૂની સલાહ નથી. વ્યક્તિગત કાનૂની પરિસ્થિતિ માટે સક્ષમ વકીલનો સંપર્ક કરો. આ વેબસાઇટ કોઈપણ સરકારી સંસ્થા સાથે જોડાયેલ નથી."
    )

    default_theme = models.CharField(
        max_length=20,
        choices=[("light", "Light Mode"), ("dark", "Dark Mode"), ("contrast", "High Contrast Accessibility")],
        default="light"
    )
    primary_accent_color = models.CharField(max_length=30, default="#B45309", help_text="Hex color code for platform primary accent")
    default_language = models.CharField(
        max_length=10,
        choices=[("gu", "ગુજરાતી (Gujarati)"), ("en", "English")],
        default="gu"
    )

    class Meta:
        verbose_name = "Site Setting & Live Legal Status"
        verbose_name_plural = "Site Settings & Live Legal Status"

    def __str__(self):
        return f"{self.site_name_en} (Status: {self.current_status})"


class UserRole:
    ADMIN = "ADMIN"
    LEGAL_REVIEWER = "LEGAL_REVIEWER"
    EDITOR = "EDITOR"

    CHOICES = [
        (ADMIN, "Platform Administrator (સંપૂર્ણ સંચાલક)"),
        (LEGAL_REVIEWER, "Legal Advocate Reviewer (કાનૂની સમીક્ષક વકીલ)"),
        (EDITOR, "Content Editor (સામગ્રી સંપાદક)"),
    ]


class UserProfile(models.Model):
    """User role and editorial profile for Custom Admin Dashboard."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=30, choices=UserRole.CHOICES, default=UserRole.EDITOR)
    bar_council_reg_number = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Bar Council Enrollment No. (Required for Legal Reviewers)"
    )
    phone_number = models.CharField(max_length=20, blank=True)
    preferred_theme = models.CharField(
        max_length=20, 
        choices=[("light", "Light Mode"), ("dark", "Dark Mode"), ("contrast", "High Contrast")],
        default="light"
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_portal_admin(self):
        return self.role == UserRole.ADMIN or self.user.is_superuser

    @property
    def is_legal_reviewer(self):
        return self.role in [UserRole.LEGAL_REVIEWER, UserRole.ADMIN] or self.user.is_superuser

    @property
    def is_editor(self):
        return True


class AuditLog(models.Model):
    """Security and compliance audit trail recording all administrative publishing and workflow actions."""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    object_repr = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Audit Log Entry"
        verbose_name_plural = "Audit Log Entries"

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.user} - {self.action} on {self.model_name}"

