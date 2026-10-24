from .models import SiteSettings, StatusTaxonomy

UI_STRINGS = {
    'en': {
        'brand_title': 'Gujarat UCC Information Platform',
        'brand_subtitle': 'Public Legal Archive & Explainer Project',
        'home': 'Home',
        'understand_ucc': 'Understand UCC',
        'topics': 'Key Topics',
        'explainers': 'Plain-Language Guides',
        'library': 'Legal Library',
        'timeline': 'Legislative Timeline',
        'news': 'News & Updates',
        'faq': 'FAQs',
        'glossary': 'Legal Glossary',
        'editorial_policy': 'Editorial Policy',
        'corrections': 'Submit Correction',
        'about': 'About Us',
        'privacy': 'Privacy Policy',
        'terms': 'Terms of Use',
        'disclaimer': 'Legal Disclaimer',
        'search': 'Search legal documents, explainers, FAQs...',
        'search_btn': 'Search',
        'last_verified': 'Last verified on',
        'verified_official_source': 'Official Legal Source',
        'status_tracker': 'Live Legislative Status',
        'source_provenance': 'Official Provenance',
        'read_more': 'Read Complete Explainer',
        'download_pdf': 'Download Official Document',
        'citations': 'Statutory Citations & References',
        'legal_reviewer': 'Reviewed by Legal Advocate',
        'who_is_covered': 'Who & What is Covered',
        'exceptions': 'Exceptions & Special Provisions',
        'what_the_law_says': 'What the Statutory Text States',
        'procedural_steps': 'Procedural Steps & Timelines',
        'misconceptions': 'Common Misconceptions Addressed',
        'explore_topics': 'Explore UCC Provisions by Subject',
        'latest_updates_head': 'Recent Legislative & Editorial Updates',
        'library_head': 'Official Gazette, Acts & Government Notifications',
        'all_rights_reserved': 'All content published under verified editorial standards. Non-governmental public legal information initiative.',
    },
    'gu': {
        'brand_title': 'ગુજરાત સમાન નાગરિક સંહિતા (UCC)',
        'brand_subtitle': 'જાહેર કાનૂની માહિતી અને માર્ગદર્શિકા મંચ',
        'home': 'મુખ્ય પૃષ્ઠ',
        'understand_ucc': 'UCC શું છે?',
        'topics': 'મુખ્ય વિષયો',
        'explainers': 'કાનૂની માર્ગદર્શિકા',
        'library': 'કાનૂની પુસ્તકાલય',
        'timeline': 'સમયરેખા (Timeline)',
        'news': 'સમાચાર અને અપડેટ્સ',
        'faq': 'સામાન્ય પ્રશ્નોત્તરી (FAQ)',
        'glossary': 'કાનૂની શબ્દકોશ',
        'editorial_policy': 'સંપાદકીય નીતિ',
        'corrections': 'ભૂલ સુધારો / પ્રતિસાદ',
        'about': 'અમારા વિશે',
        'privacy': 'ગોપનીયતા નીતિ',
        'terms': 'ઉપયોગની શરતો',
        'disclaimer': 'કાનૂની અસ્વીકરણ',
        'search': 'કાયદાકીય દસ્તાવેજો, માર્ગદર્શિકા, પ્રશ્નો શોધો...',
        'search_btn': 'શોધો',
        'last_verified': 'છેલ્લી ચકાસણી તારીખ',
        'verified_official_source': 'સત્તાવાર કાનૂની સ્ત્રોત',
        'status_tracker': 'કાયદાકીય સ્થિતિ (Live Status)',
        'source_provenance': 'સત્તાવાર સ્ત્રોત સંદર્ભ',
        'read_more': 'સંપૂર્ણ માર્ગદર્શિકા વાંચો',
        'download_pdf': 'સત્તાવાર દસ્તાવેજ ડાઉનલોડ કરો',
        'citations': 'વૈધાનિક કલમો અને સંદર્ભો',
        'legal_reviewer': 'કાનૂની સમીક્ષક વકીલ',
        'who_is_covered': 'કોના પર અને શું લાગુ પડશે?',
        'exceptions': 'અપવાદો અને વિશેષ જોગવાઈઓ',
        'what_the_law_says': 'કાયદાની મૂળ કલમો શું કહે છે?',
        'procedural_steps': 'કાર્યપદ્ધતિ અને નિયમોના તબક્કા',
        'misconceptions': 'સામાન્ય ગેરમાન્યતાઓ અને સાચી માહિતી',
        'explore_topics': 'વિષયવાર UCC જોગવાઈઓ સમજો',
        'latest_updates_head': 'તાજા કાયદાકીય અને સંપાદકીય સમાચાર',
        'library_head': 'સત્તાવાર અસાધારણ ગેઝેટ, વિધેયક અને જાહેરનામા',
        'all_rights_reserved': 'ચકાસાયેલ સંપાદકીય ધોરણો હેઠળ પ્રકાશિત. બિન-સરકારી સ્વતંત્ર જાહેર કાનૂની માહિતી પહેલ.',
    }
}


def site_context(request):
    """Provides current language, UI strings, and global site status to all templates."""
    current_lang = getattr(request, 'site_lang', 'gu')
    is_gujarati = (current_lang == 'gu')
    
    # Get or create default site settings
    settings = SiteSettings.objects.first()
    if not settings:
        import datetime
        settings = SiteSettings.objects.create(
            last_verified_date=datetime.date(2026, 10, 24)
        )
    
    # Get current status badge and label
    status_key = settings.current_status
    status_label = StatusTaxonomy.LABELS_GU.get(status_key) if is_gujarati else StatusTaxonomy.LABELS_EN.get(status_key)
    status_badge_class = StatusTaxonomy.BADGE_CLASSES.get(status_key, 'status-badge-neutral')
    
    # Get current theme and accent
    default_theme = getattr(settings, 'default_theme', 'light') if settings else 'light'
    current_theme = request.session.get('site_theme', default_theme)
    primary_accent = getattr(settings, 'primary_accent_color', '#B45309') if settings else '#B45309'

    user_profile = None
    if request.user.is_authenticated:
        try:
            from apps.core.models import UserProfile, UserRole
            user_profile, _ = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={'role': UserRole.ADMIN if request.user.is_superuser else UserRole.EDITOR}
            )
        except Exception:
            user_profile = None

    return {
        'current_lang': current_lang,
        'is_gujarati': is_gujarati,
        'ui': UI_STRINGS.get(current_lang, UI_STRINGS['gu']),
        'site_settings': settings,
        'current_status_label': status_label,
        'current_status_badge_class': status_badge_class,
        'current_theme': current_theme,
        'primary_accent_color': primary_accent,
        'user_profile': user_profile,
        'STATUS_LABELS_EN': StatusTaxonomy.LABELS_EN,
        'STATUS_LABELS_GU': StatusTaxonomy.LABELS_GU,
        'STATUS_BADGE_CLASSES': StatusTaxonomy.BADGE_CLASSES,
    }

