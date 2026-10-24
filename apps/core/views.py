from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.topics.models import Topic
from apps.explainers.models import Explainer
from apps.library.models import LegalDocument
from apps.timeline.models import TimelineEvent
from apps.news.models import NewsArticle
from apps.glossary_faq.models import FAQ, GlossaryTerm


def home(request):
    """
    Public Homepage adhering to Section 4 & Image 2 (News Portal) specification:
    Headline/status banner, latest verified update, key topics, latest news,
    explainers, official documents, timeline snippet, source transparency.
    """
    topics = Topic.objects.filter(is_active=True).order_by('order')
    
    # News & Updates
    breaking_news = NewsArticle.objects.filter(is_breaking=True).first()
    recent_news = NewsArticle.objects.exclude(id=breaking_news.id if breaking_news else None)[:4]
    
    # Featured explainers & documents
    featured_explainers = Explainer.objects.filter(editorial_status='PUBLISHED')[:4]
    official_documents = LegalDocument.objects.all()[:5]
    
    # Timeline snippet
    recent_milestones = TimelineEvent.objects.all().order_by('-event_date')[:4]
    
    # Featured FAQs
    featured_faqs = FAQ.objects.filter(is_published=True, is_featured=True)[:4]
    if not featured_faqs.exists():
        featured_faqs = FAQ.objects.filter(is_published=True)[:4]

    context = {
        'topics': topics,
        'breaking_news': breaking_news,
        'recent_news': recent_news,
        'featured_explainers': featured_explainers,
        'official_documents': official_documents,
        'recent_milestones': recent_milestones,
        'featured_faqs': featured_faqs,
    }
    return render(request, 'pages/home.html', context)


def understand_ucc(request):
    """Introductory overview: What UCC means, scope, Gujarat Act coverage, exclusions, misconceptions."""
    topics = Topic.objects.filter(is_active=True).order_by('order')
    return render(request, 'pages/understand_ucc.html', {'topics': topics})


def about_page(request):
    """About the platform, non-governmental public mandate, editorial ethics, and team."""
    return render(request, 'pages/about_editorial_policy.html', {'active_tab': 'about'})


def editorial_policy(request):
    """Editorial standards, review workflow, citation hierarchy, and correction policy."""
    return render(request, 'pages/about_editorial_policy.html', {'active_tab': 'policy'})


def privacy_policy(request):
    """Strict privacy policy: Zero sensitive personal case intake in V1."""
    return render(request, 'pages/privacy_policy.html')


def terms_page(request):
    """Terms of use, legal disclaimers, and copyright policies."""
    return render(request, 'pages/terms_page.html')


def search_page(request):
    """Global search across explainers, documents, news, FAQs, and glossary."""
    query = request.GET.get('q', '').strip()
    explainer_results = []
    doc_results = []
    news_results = []
    faq_results = []
    glossary_results = []

    if query:
        explainer_results = Explainer.objects.filter(
            Q(title_en__icontains=query) | Q(title_gu__icontains=query) |
            Q(summary_deck_en__icontains=query) | Q(summary_deck_gu__icontains=query) |
            Q(what_the_text_says_en__icontains=query) | Q(what_the_text_says_gu__icontains=query)
        )[:10]

        doc_results = LegalDocument.objects.filter(
            Q(title_en__icontains=query) | Q(title_gu__icontains=query) |
            Q(document_number__icontains=query) | Q(summary_en__icontains=query) | Q(summary_gu__icontains=query)
        )[:10]

        news_results = NewsArticle.objects.filter(
            Q(headline_en__icontains=query) | Q(headline_gu__icontains=query) |
            Q(body_en__icontains=query) | Q(body_gu__icontains=query)
        )[:10]

        faq_results = FAQ.objects.filter(
            Q(question_en__icontains=query) | Q(question_gu__icontains=query) |
            Q(short_answer_en__icontains=query) | Q(short_answer_gu__icontains=query)
        )[:10]

        glossary_results = GlossaryTerm.objects.filter(
            Q(term_en__icontains=query) | Q(term_gu__icontains=query) |
            Q(plain_language_definition_en__icontains=query) | Q(plain_language_definition_gu__icontains=query)
        )[:10]

    context = {
        'query': query,
        'explainer_results': explainer_results,
        'doc_results': doc_results,
        'news_results': news_results,
        'faq_results': faq_results,
        'glossary_results': glossary_results,
        'total_results': len(explainer_results) + len(doc_results) + len(news_results) + len(faq_results) + len(glossary_results)
    }
    return render(request, 'pages/search_results.html', context)
