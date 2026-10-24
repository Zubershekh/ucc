import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from apps.core.models import (
    SiteSettings, StatusTaxonomy, EditorialStatus, AuditLog,
    UserProfile, UserRole
)
from apps.topics.models import Topic
from apps.explainers.models import Explainer
from apps.library.models import LegalDocument, DocumentType
from apps.news.models import NewsArticle, NewsCategory
from apps.glossary_faq.models import FAQ, GlossaryTerm
from apps.corrections.models import CorrectionReport, CorrectionStatus


class PublicPlatformTests(TestCase):
    """Test suite verifying public pages, Gujarati-first default, and verified citations."""

    def setUp(self):
        self.client = Client()
        self.settings = SiteSettings.objects.create(
            site_name_gu="ગુજરાત સમાન નાગરિક સંહિતા માહિતી મંચ",
            site_name_en="Gujarat UCC Information Platform",
            current_status=StatusTaxonomy.PUBLISHED_IN_GAZETTE,
            last_verified_date=datetime.date(2026, 10, 24),
            default_language="gu",
            default_theme="light",
        )
        self.topic = Topic.objects.create(
            name_gu="લગ્ન અને નોંધણી",
            name_en="Marriage and Registration",
            slug="marriage-registration",
            summary_gu="તમામ લગ્નોની ફરજિયાત નોંધણી.",
            summary_en="Mandatory registration of all marriages.",
            order=1,
            is_active=True
        )
        self.doc = LegalDocument.objects.create(
            title_gu="ગુજરાત સમાન નાગરિક સંહિતા અધિનિયમ, ૨૦૨૬",
            title_en="The Gujarat Uniform Civil Code Act, 2026",
            slug="gujarat-ucc-act-2026",
            document_type=DocumentType.GAZETTE,
            document_number="Act No. 17 of 2026",
            publication_date=datetime.date(2026, 10, 1),
            summary_gu="અસાધારણ ગેઝેટ વોલ્યુમ LXVII",
            summary_en="Extraordinary Gazette Vol LXVII"
        )
        self.explainer = Explainer.objects.create(
            title_gu="લગ્ન નોંધણી પ્રક્રિયા અને શરતો",
            title_en="Marriage Registration Procedure and Rules",
            slug="marriage-registration-procedure",
            topic=self.topic,
            summary_deck_gu="લગ્નની ફરજિયાત નોંધણી અંગેની સંપૂર્ણ માર્ગદર્શિકા.",
            summary_deck_en="Comprehensive guide on mandatory marriage registration.",
            what_the_text_says_gu="તમામ સમુદાયો માટે સમાન કાનૂની વય.",
            what_the_text_says_en="Uniform age of marriage across communities.",
            who_is_covered_gu="ગુજરાત રાજ્યના તમામ નાગરિકો.",
            who_is_covered_en="All residents of Gujarat.",
            exceptions_gu="કોઈ અપવાદ નથી.",
            exceptions_en="No exemptions.",
            source_citations="Section 8 & 9 of Gujarat Act 17 of 2026",
            legal_status_badge=StatusTaxonomy.PUBLISHED_IN_GAZETTE,
            editorial_status=EditorialStatus.PUBLISHED,
            legal_reviewer_name="Adv. H. S. Trivedi (Legal QA)",
            last_verified_date=datetime.date(2026, 10, 24)
        )

    def test_homepage_gujarati_default(self):
        """Verify homepage returns 200, defaults to Gujarati and renders bold hero."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lang="gu"')
        self.assertContains(response, "ગુજરાત સમાન નાગરિક સંહિતા (UCC) ૨૦૨૬")
        self.assertContains(response, "ગેઝેટમાં પ્રકાશિત")

    def test_homepage_english_toggle(self):
        """Verify ?lang=en toggles language correctly."""
        response = self.client.get(reverse('home') + '?lang=en')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lang="en"')
        self.assertContains(response, "Gujarat Uniform Civil Code, 2026")

    def test_strict_light_mode_enforced(self):
        """Verify light mode is strictly enforced and dark theme is ignored."""
        response = self.client.get(reverse('home') + '?theme=dark')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'theme-light')
        self.assertNotContains(response, 'theme-dark')
        self.assertEqual(self.client.session.get('site_theme'), 'light')

    def test_topic_detail_page(self):
        """Verify dedicated topic page loads with full context."""
        response = self.client.get(reverse('topic_detail', kwargs={'slug': self.topic.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.topic.title_gu)

    def test_explainer_detail_page(self):
        """Verify dedicated explainer page loads with statutory citations and advocate QA."""
        response = self.client.get(reverse('explainer_detail', kwargs={'slug': self.explainer.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.explainer.title_gu)
        self.assertContains(response, "Section 8 &amp; 9 of Gujarat Act 17 of 2026")
        self.assertContains(response, "Adv. H. S. Trivedi")

    def test_library_and_timeline_pages(self):
        """Verify library, timeline, news, and faq pages load successfully."""
        for url_name in ['library_list', 'timeline_page', 'news_list', 'faq_glossary']:
            res = self.client.get(reverse(url_name))
            self.assertEqual(res.status_code, 200, f"Failed on {url_name}")

    def test_corrections_form_submission(self):
        """Verify citizen correction intake submits and saves to database."""
        post_data = {
            'reference_page_or_topic': 'Succession Section 14',
            'correction_type': 'FACTUAL_ERROR',
            'specific_error_description': 'Typo in clause 3 citation.',
            'suggested_correction': 'Replace Section 13 with Section 14.',
            'official_source_proof': 'Gujarat Gazette Vol LXVII, page 12',
            'submitter_name': 'Ramesh Patel',
            'submitter_email': 'ramesh@example.com'
        }
        res = self.client.post(reverse('corrections_page'), post_data)
        self.assertEqual(res.status_code, 302)  # Redirects with success flash message
        self.assertTrue(CorrectionReport.objects.filter(reference_page_or_topic='Succession Section 14').exists())


class PortalAdminDashboardTests(TestCase):
    """Test suite verifying Custom Admin Dashboard, Legal QA Workflow, Roles, and Audit Trail."""

    def setUp(self):
        self.client = Client()
        # Create users with different roles
        self.admin_user = User.objects.create_superuser(
            username='admin_boss', password='password123', email='admin@ucc.org'
        )
        self.admin_profile = UserProfile.objects.create(
            user=self.admin_user, role=UserRole.ADMIN
        )

        self.legal_user = User.objects.create_user(
            username='advocate_qa', password='password123', email='advocate@ucc.org', is_staff=True
        )
        self.legal_profile = UserProfile.objects.create(
            user=self.legal_user, role=UserRole.LEGAL_REVIEWER, bar_council_reg_number='G/1842/2012'
        )

        self.editor_user = User.objects.create_user(
            username='writer_editor', password='password123', email='editor@ucc.org', is_staff=True
        )
        self.editor_profile = UserProfile.objects.create(
            user=self.editor_user, role=UserRole.EDITOR
        )

        self.settings = SiteSettings.objects.create(
            site_name_gu="ગુજરાત સમાન નાગરિક સંહિતા",
            current_status=StatusTaxonomy.PUBLISHED_IN_GAZETTE,
            last_verified_date=datetime.date(2026, 10, 24),
            default_language="gu",
            default_theme="light"
        )
        self.topic = Topic.objects.create(
            name_gu="વારસાઈ", name_en="Succession", slug="succession-test", order=1
        )
        self.draft_explainer = Explainer.objects.create(
            title_gu="વારસાઈ કાયદો ખરડો",
            title_en="Succession Law Draft",
            slug="succession-draft",
            topic=self.topic,
            summary_deck_gu="ખરડો સારાંશ.",
            summary_deck_en="Draft summary.",
            what_the_text_says_gu="કલમો.",
            what_the_text_says_en="Clauses.",
            who_is_covered_gu="બધા.",
            who_is_covered_en="All.",
            exceptions_gu="નથી.",
            exceptions_en="None.",
            source_citations="Section 14 Act 17 of 2026",
            editorial_status=EditorialStatus.DRAFT,
            last_verified_date=datetime.date(2026, 10, 24)
        )

    def test_unauthenticated_admin_redirect(self):
        """Verify unauthenticated user cannot access /portal-admin/."""
        res = self.client.get(reverse('portal_admin_home'))
        self.assertEqual(res.status_code, 302)
        self.assertIn('/portal-admin/login/', res.url)

    def test_admin_login_and_dashboard(self):
        """Verify login works and dashboard renders KPI metrics."""
        login_res = self.client.post(reverse('portal_admin_login'), {
            'username': 'admin_boss',
            'password': 'password123'
        })
        self.assertEqual(login_res.status_code, 302)

        # Access dashboard
        dash_res = self.client.get(reverse('portal_admin_home'))
        self.assertEqual(dash_res.status_code, 200)
        self.assertContains(dash_res, "Command Center")
        self.assertContains(dash_res, "Live Legal Status")

    def test_update_legal_status_action_and_audit_log(self):
        """Verify updating platform status persists and generates AuditLog."""
        self.client.login(username='admin_boss', password='password123')
        post_data = {
            'update_legal_status': '1',
            'current_status': StatusTaxonomy.COMMENCEMENT_NOTIFIED,
            'status_summary_gu': 'નવું અમલવારી જાહેરનામું પ્રસિદ્ધ થયું.',
            'status_summary_en': 'Commencement notification published by State Govt.',
            'last_verified_date': '2026-10-25'
        }
        res = self.client.post(reverse('portal_admin_home'), post_data)
        self.assertEqual(res.status_code, 302)

        # Verify database updated
        self.settings.refresh_from_db()
        self.assertEqual(self.settings.current_status, StatusTaxonomy.COMMENCEMENT_NOTIFIED)

        # Verify AuditLog created
        audit = AuditLog.objects.filter(action='UPDATE_LEGAL_STATUS').first()
        self.assertIsNotNone(audit)
        self.assertEqual(audit.user, self.admin_user)

    def test_legal_review_workflow_transition(self):
        """Verify legal advocate can approve an explainer and transition it to APPROVED."""
        self.client.login(username='advocate_qa', password='password123')

        # 1. First move draft to LEGAL_REVIEW
        self.draft_explainer.editorial_status = EditorialStatus.LEGAL_REVIEW
        self.draft_explainer.save()

        # 2. Advocate approves
        post_data = {
            'transition_status': '1',
            'explainer_id': self.draft_explainer.id,
            'new_status': EditorialStatus.APPROVED,
            'reviewer_notes': 'Verified against Gazette Vol LXVII, section 14 matches.',
            'reviewer_name': 'Adv. H. S. Trivedi (G/1842/2012)'
        }
        res = self.client.post(reverse('portal_admin_review_queue'), post_data)
        self.assertEqual(res.status_code, 302)

        self.draft_explainer.refresh_from_db()
        self.assertEqual(self.draft_explainer.editorial_status, EditorialStatus.APPROVED)

        # Verify audit log captures advocate notes
        audit = AuditLog.objects.filter(action='WORKFLOW_TRANSITION', object_id=str(self.draft_explainer.id)).first()
        self.assertIsNotNone(audit)
        self.assertIn("Verified against Gazette", audit.notes)

    def test_editor_cannot_approve_content(self):
        """Verify standard Editor role cannot approve content without advocate review."""
        self.client.login(username='writer_editor', password='password123')
        self.draft_explainer.editorial_status = EditorialStatus.LEGAL_REVIEW
        self.draft_explainer.save()

        post_data = {
            'transition_status': '1',
            'explainer_id': self.draft_explainer.id,
            'new_status': EditorialStatus.APPROVED,
        }
        res = self.client.post(reverse('portal_admin_review_queue'), post_data)
        self.assertEqual(res.status_code, 302)

        # Must NOT be approved
        self.draft_explainer.refresh_from_db()
        self.assertEqual(self.draft_explainer.editorial_status, EditorialStatus.LEGAL_REVIEW)

    def test_appearance_and_language_settings_persistence(self):
        """Verify platform settings enforce light theme and save preferences."""
        self.client.login(username='admin_boss', password='password123')
        post_data = {
            'default_theme': 'light',
            'primary_accent_color': '#059669',
            'default_language': 'gu',
            'announcement_banner_gu': 'નવું જાહેરનામું ટૂંક સમયમાં અપેક્ષિત છે.',
            'show_announcement': 'on',
            'verified_official_source_url': 'https://cms.neva.gov.in/test.pdf'
        }
        res = self.client.post(reverse('portal_admin_settings'), post_data)
        self.assertEqual(res.status_code, 302)

        self.settings.refresh_from_db()
        self.assertEqual(self.settings.default_theme, 'light')
        self.assertEqual(self.settings.primary_accent_color, '#059669')
        self.assertEqual(self.settings.announcement_banner_gu, 'નવું જાહેરનામું ટૂંક સમયમાં અપેક્ષિત છે.')

    def test_role_management_restricted_to_admin(self):
        """Verify only Admin can change roles in /portal-admin/roles/."""
        # Editor attempts access -> denied
        self.client.login(username='writer_editor', password='password123')
        res = self.client.get(reverse('portal_admin_roles'))
        self.assertEqual(res.status_code, 302)

        # Admin accesses -> 200
        self.client.login(username='admin_boss', password='password123')
        res_admin = self.client.get(reverse('portal_admin_roles'))
        self.assertEqual(res_admin.status_code, 200)
        self.assertContains(res_admin, "User Roles &amp; Permissions")
