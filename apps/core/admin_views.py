"""
Custom Admin & Editorial CMS Dashboard for Gujarat UCC Platform.
Adheres to Section 5 (Editorial Workflow), Section 8 (Roles & Security),
and Section 10 (Audit Trail & Verification Standards).
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from functools import wraps

from apps.core.models import (
    SiteSettings, StatusTaxonomy, EditorialStatus, AuditLog,
    UserProfile, UserRole
)
from apps.topics.models import Topic
from apps.explainers.models import Explainer
from apps.library.models import LegalDocument
from apps.news.models import NewsArticle
from apps.glossary_faq.models import FAQ, GlossaryTerm
from apps.corrections.models import CorrectionReport, CorrectionStatus


# ==============================================================================
# Permission Decorators
# ==============================================================================

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def log_admin_action(user, action, model_name, object_id='', object_repr='', ip='', notes=''):
    try:
        AuditLog.objects.create(
            user=user if user.is_authenticated else None,
            action=action,
            model_name=model_name,
            object_id=str(object_id),
            object_repr=str(object_repr)[:250],
            ip_address=ip or None,
            notes=notes
        )
    except Exception as e:
        print(f"Error logging audit action: {e}")


def portal_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('portal_admin_login')
        if not (request.user.is_staff or request.user.is_superuser or hasattr(request.user, 'profile')):
            messages.error(request, "Access denied. You do not have editorial privileges.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('portal_admin_login')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            profile = getattr(request.user, 'profile', None)
            if not profile or profile.role not in allowed_roles:
                messages.error(request, f"Access restricted. Required role: {', '.join(allowed_roles)}")
                return redirect('portal_admin_home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# ==============================================================================
# Authentication Views
# ==============================================================================

def portal_login_view(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('portal_admin_home')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            ip = get_client_ip(request)
            log_admin_action(user, "USER_LOGIN", "User", user.id, user.username, ip=ip, notes="Logged in to Portal Admin")
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('portal_admin_home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'portal_admin/login.html')


def portal_logout_view(request):
    if request.user.is_authenticated:
        ip = get_client_ip(request)
        log_admin_action(request.user, "USER_LOGOUT", "User", request.user.id, request.user.username, ip=ip, notes="Logged out")
        logout(request)
    messages.info(request, "You have been securely signed out.")
    return redirect('portal_admin_login')


# ==============================================================================
# 1. Main Dashboard Overview
# ==============================================================================

@portal_admin_required
def admin_dashboard_home(request):
    """Command Center: Metrics, Legal Review Queue, Quick Status Update & Recent Audits."""
    settings = SiteSettings.objects.first()
    ip = get_client_ip(request)

    # Handle quick status update
    if request.method == "POST" and "update_legal_status" in request.POST:
        new_status = request.POST.get("current_status")
        summary_gu = request.POST.get("status_summary_gu", "").strip()
        summary_en = request.POST.get("status_summary_en", "").strip()
        last_verified = request.POST.get("last_verified_date")

        if settings and new_status in dict(StatusTaxonomy.CHOICES):
            old_status = settings.current_status
            settings.current_status = new_status
            if summary_gu:
                settings.status_summary_gu = summary_gu
            if summary_en:
                settings.status_summary_en = summary_en
            if last_verified:
                settings.last_verified_date = last_verified
            settings.save()

            log_admin_action(
                request.user, "UPDATE_LEGAL_STATUS", "SiteSettings", settings.id,
                f"Changed from {old_status} to {new_status}", ip=ip,
                notes=f"Updated public legal status to {new_status}"
            )
            messages.success(request, f"Platform legal status updated to: {settings.get_current_status_display()}")
            return redirect('portal_admin_home')

    # Metrics
    kpis = {
        'total_topics': Topic.objects.count(),
        'total_explainers': Explainer.objects.count(),
        'published_explainers': Explainer.objects.filter(editorial_status=EditorialStatus.PUBLISHED).count(),
        'pending_legal_review': Explainer.objects.filter(editorial_status=EditorialStatus.LEGAL_REVIEW).count(),
        'total_documents': LegalDocument.objects.count(),
        'total_news': NewsArticle.objects.count(),
        'pending_corrections': CorrectionReport.objects.filter(status=CorrectionStatus.PENDING).count(),
        'total_faqs': FAQ.objects.count(),
    }

    # Queue items awaiting legal advocate sign-off
    review_queue = Explainer.objects.filter(
        editorial_status__in=[EditorialStatus.DRAFT, EditorialStatus.IN_REVIEW, EditorialStatus.LEGAL_REVIEW]
    ).select_related('topic').order_by('-id')[:5]

    # Recent Audit activity
    recent_audits = AuditLog.objects.select_related('user').order_by('-timestamp')[:8]

    # Pending citizen correction reports
    pending_corrections_list = CorrectionReport.objects.filter(
        status=CorrectionStatus.PENDING
    ).order_by('-created_at')[:4]

    return render(request, 'portal_admin/dashboard.html', {
        'site_settings': settings,
        'kpis': kpis,
        'review_queue': review_queue,
        'recent_audits': recent_audits,
        'pending_corrections_list': pending_corrections_list,
        'status_choices': StatusTaxonomy.CHOICES,
    })


# ==============================================================================
# 2. Content Management Hub (Topics, Explainers, Library, News, FAQs)
# ==============================================================================

@portal_admin_required
def admin_content_list(request):
    """Tabbed management view for all educational and legal platform items."""
    tab = request.GET.get('tab', 'explainers')
    search_q = request.GET.get('q', '').strip()

    explainers = Explainer.objects.select_related('topic').order_by('-id')
    topics = Topic.objects.all().order_by('order')
    documents = LegalDocument.objects.all().order_by('-publication_date')
    news_items = NewsArticle.objects.all().order_by('-published_date')
    faqs = FAQ.objects.all().order_by('order')

    if search_q:
        explainers = explainers.filter(title_gu__icontains=search_q) | explainers.filter(title_en__icontains=search_q)
        topics = topics.filter(title_gu__icontains=search_q) | topics.filter(title_en__icontains=search_q)
        documents = documents.filter(title_gu__icontains=search_q) | documents.filter(title_en__icontains=search_q)
        news_items = news_items.filter(title_gu__icontains=search_q) | news_items.filter(title_en__icontains=search_q)
        faqs = faqs.filter(question_gu__icontains=search_q) | faqs.filter(question_en__icontains=search_q)

    return render(request, 'portal_admin/content_list.html', {
        'active_tab': tab,
        'search_q': search_q,
        'explainers': explainers,
        'topics': topics,
        'documents': documents,
        'news_items': news_items,
        'faqs': faqs,
    })


@portal_admin_required
def admin_explainer_edit(request, pk=None):
    """Create or edit plain-language legal explainer with bilingual fields and citations."""
    explainer = get_object_or_404(Explainer, pk=pk) if pk else None
    ip = get_client_ip(request)

    if request.method == "POST":
        title_gu = request.POST.get('title_gu', '').strip()
        title_en = request.POST.get('title_en', '').strip()
        topic_id = request.POST.get('topic_id')
        summary_deck_gu = request.POST.get('summary_deck_gu', '').strip()
        summary_deck_en = request.POST.get('summary_deck_en', '').strip()
        what_the_text_says_gu = request.POST.get('what_the_text_says_gu', '').strip()
        what_the_text_says_en = request.POST.get('what_the_text_says_en', '').strip()
        who_is_covered_gu = request.POST.get('who_is_covered_gu', '').strip()
        who_is_covered_en = request.POST.get('who_is_covered_en', '').strip()
        exceptions_gu = request.POST.get('exceptions_gu', '').strip()
        exceptions_en = request.POST.get('exceptions_en', '').strip()
        source_citations = request.POST.get('source_citations', '').strip()
        legal_status_badge = request.POST.get('legal_status_badge', StatusTaxonomy.PUBLISHED_IN_GAZETTE)
        editorial_status = request.POST.get('editorial_status', EditorialStatus.DRAFT)
        legal_reviewer_name = request.POST.get('legal_reviewer_name', '').strip()

        topic = get_object_or_404(Topic, pk=topic_id)

        if not explainer:
            # Create new slug
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(title_en) or f"explainer-{uuid.uuid4().hex[:6]}"
            slug = base_slug
            counter = 1
            while Explainer.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            explainer = Explainer.objects.create(
                title_gu=title_gu,
                title_en=title_en,
                slug=slug,
                topic=topic,
                summary_deck_gu=summary_deck_gu,
                summary_deck_en=summary_deck_en,
                what_the_text_says_gu=what_the_text_says_gu,
                what_the_text_says_en=what_the_text_says_en,
                who_is_covered_gu=who_is_covered_gu,
                who_is_covered_en=who_is_covered_en,
                exceptions_gu=exceptions_gu,
                exceptions_en=exceptions_en,
                source_citations=source_citations,
                legal_status_badge=legal_status_badge,
                editorial_status=editorial_status,
                legal_reviewer_name=legal_reviewer_name,
                author_name=request.user.get_full_name() or request.user.username,
                last_verified_date=timezone.now().date(),
            )
            log_admin_action(request.user, "CREATE_EXPLAINER", "Explainer", explainer.id, explainer.title_gu, ip=ip)
            messages.success(request, f"New explainer '{explainer.title_gu}' created successfully.")
        else:
            explainer.title_gu = title_gu
            explainer.title_en = title_en
            explainer.topic = topic
            explainer.summary_deck_gu = summary_deck_gu
            explainer.summary_deck_en = summary_deck_en
            explainer.what_the_text_says_gu = what_the_text_says_gu
            explainer.what_the_text_says_en = what_the_text_says_en
            explainer.who_is_covered_gu = who_is_covered_gu
            explainer.who_is_covered_en = who_is_covered_en
            explainer.exceptions_gu = exceptions_gu
            explainer.exceptions_en = exceptions_en
            explainer.source_citations = source_citations
            explainer.legal_status_badge = legal_status_badge
            explainer.editorial_status = editorial_status
            if legal_reviewer_name:
                explainer.legal_reviewer_name = legal_reviewer_name
            explainer.save()

            log_admin_action(request.user, "UPDATE_EXPLAINER", "Explainer", explainer.id, explainer.title_gu, ip=ip)
            messages.success(request, f"Explainer '{explainer.title_gu}' updated successfully.")

        return redirect('portal_admin_content')

    topics = Topic.objects.all().order_by('order')
    return render(request, 'portal_admin/explainer_form.html', {
        'explainer': explainer,
        'topics': topics,
        'status_choices': StatusTaxonomy.CHOICES,
        'editorial_choices': EditorialStatus.CHOICES,
    })


# ==============================================================================
# 3. Dedicated Legal Review Workflow Queue
# ==============================================================================

@portal_admin_required
def admin_review_queue(request):
    """
    Legal Advocate QA and Editorial Lifecycle Board:
    Draft -> Legal Review -> Approved -> Published.
    Allows advocates to review statutory citations and verify text accuracy.
    """
    ip = get_client_ip(request)

    if request.method == "POST" and "transition_status" in request.POST:
        explainer_id = request.POST.get('explainer_id')
        new_status = request.POST.get('new_status')
        reviewer_notes = request.POST.get('reviewer_notes', '').strip()
        reviewer_name = request.POST.get('reviewer_name', '').strip()

        explainer = get_object_or_404(Explainer, id=explainer_id)
        old_status = explainer.editorial_status

        # Enforce role check: Only Legal Reviewers or Admins can Approve
        profile = getattr(request.user, 'profile', None)
        if new_status in [EditorialStatus.APPROVED, EditorialStatus.PUBLISHED]:
            if not (request.user.is_superuser or (profile and profile.is_legal_reviewer)):
                messages.error(request, "Permission denied: Only qualified Legal Advocate Reviewers can approve content.")
                return redirect('portal_admin_review_queue')

        explainer.editorial_status = new_status
        if reviewer_name:
            explainer.legal_reviewer_name = reviewer_name
        explainer.save()

        log_notes = f"Transitioned from {old_status} to {new_status}."
        if reviewer_notes:
            log_notes += f" Advocate QA Notes: {reviewer_notes}"

        log_admin_action(
            request.user, "WORKFLOW_TRANSITION", "Explainer",
            explainer.id, explainer.title_gu, ip=ip, notes=log_notes
        )
        messages.success(request, f"Explainer '{explainer.title_gu}' moved to {explainer.get_editorial_status_display()}.")
        return redirect('portal_admin_review_queue')

    # Group explainers by workflow stages
    drafts = Explainer.objects.filter(editorial_status=EditorialStatus.DRAFT).select_related('topic')
    in_review = Explainer.objects.filter(editorial_status=EditorialStatus.IN_REVIEW).select_related('topic')
    legal_review = Explainer.objects.filter(editorial_status=EditorialStatus.LEGAL_REVIEW).select_related('topic')
    approved = Explainer.objects.filter(editorial_status=EditorialStatus.APPROVED).select_related('topic')
    published = Explainer.objects.filter(editorial_status=EditorialStatus.PUBLISHED).select_related('topic')[:10]

    return render(request, 'portal_admin/review_queue.html', {
        'drafts': drafts,
        'in_review': in_review,
        'legal_review': legal_review,
        'approved': approved,
        'published': published,
        'editorial_choices': EditorialStatus.CHOICES,
    })


# ==============================================================================
# 4. Theme & Language Management
# ==============================================================================

@portal_admin_required
def admin_settings_view(request):
    """Manage global theme controls, primary accent color, default language, and site notices."""
    settings = SiteSettings.objects.first()
    ip = get_client_ip(request)

    if request.method == "POST":
        default_theme = request.POST.get('default_theme', 'light')
        primary_accent_color = request.POST.get('primary_accent_color', '#B45309')
        default_language = request.POST.get('default_language', 'gu')
        announcement_gu = request.POST.get('announcement_banner_gu', '').strip()
        announcement_en = request.POST.get('announcement_banner_en', '').strip()
        show_announcement = 'show_announcement' in request.POST
        official_source_url = request.POST.get('verified_official_source_url', '').strip()

        if settings:
            settings.default_theme = default_theme
            settings.primary_accent_color = primary_accent_color
            settings.default_language = default_language
            settings.announcement_banner_gu = announcement_gu
            settings.announcement_banner_en = announcement_en
            settings.show_announcement = show_announcement
            if official_source_url:
                settings.verified_official_source_url = official_source_url
            settings.save()

            # Update session theme immediately
            request.session['site_theme'] = default_theme

            log_admin_action(
                request.user, "UPDATE_THEME_LANGUAGE_SETTINGS", "SiteSettings",
                settings.id, "Platform Settings", ip=ip,
                notes=f"Theme set to {default_theme}, Accent to {primary_accent_color}, Default Lang to {default_language}"
            )
            messages.success(request, "Theme and Language preferences saved successfully.")
            return redirect('portal_admin_settings')

    return render(request, 'portal_admin/settings.html', {
        'site_settings': settings,
    })


# ==============================================================================
# 5. User Roles & Permission Management
# ==============================================================================

@portal_admin_required
@role_required([UserRole.ADMIN])
def admin_roles_view(request):
    """Administrator access to assign User Roles and Bar Council registration numbers."""
    ip = get_client_ip(request)

    if request.method == "POST" and "update_user_role" in request.POST:
        target_user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        bar_council_no = request.POST.get('bar_council_reg_number', '').strip()

        target_user = get_object_or_404(User, id=target_user_id)
        profile, _ = UserProfile.objects.get_or_create(user=target_user)

        old_role = profile.role
        profile.role = new_role
        profile.bar_council_reg_number = bar_council_no
        profile.save()

        # If role is ADMIN or LEGAL_REVIEWER, give staff status
        if new_role in [UserRole.ADMIN, UserRole.LEGAL_REVIEWER]:
            target_user.is_staff = True
            target_user.save()

        log_admin_action(
            request.user, "UPDATE_USER_ROLE", "User", target_user.id,
            target_user.username, ip=ip,
            notes=f"Changed role from {old_role} to {new_role}. Bar Council No: {bar_council_no}"
        )
        messages.success(request, f"Updated role for {target_user.username} to {profile.get_role_display()}.")
        return redirect('portal_admin_roles')

    users = User.objects.all().select_related('profile').order_by('-is_superuser', 'username')
    return render(request, 'portal_admin/roles.html', {
        'users': users,
        'role_choices': UserRole.CHOICES,
    })


# ==============================================================================
# 6. Audit Logs View
# ==============================================================================

@portal_admin_required
def admin_audit_logs_view(request):
    """Compliance & security audit log viewer with search, action filtering and timestamps."""
    action_filter = request.GET.get('action', '').strip()
    search_q = request.GET.get('q', '').strip()

    logs = AuditLog.objects.select_related('user').order_by('-timestamp')

    if action_filter:
        logs = logs.filter(action=action_filter)
    if search_q:
        logs = logs.filter(object_repr__icontains=search_q) | logs.filter(notes__icontains=search_q) | logs.filter(user__username__icontains=search_q)

    # Get distinct actions for filter dropdown
    distinct_actions = AuditLog.objects.values_list('action', flat=True).distinct()[:15]

    return render(request, 'portal_admin/audit_logs.html', {
        'logs': logs[:100],
        'action_filter': action_filter,
        'search_q': search_q,
        'distinct_actions': distinct_actions,
    })
