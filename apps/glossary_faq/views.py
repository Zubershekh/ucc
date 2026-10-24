from django.shortcuts import render
from .models import FAQ, GlossaryTerm
from apps.topics.models import Topic


def faq_glossary(request):
    """
    Searchable question-and-answer repository and plain-language
    legal glossary with bilingual equivalents.
    """
    faqs = FAQ.objects.filter(is_published=True).order_by('order')
    glossary_terms = GlossaryTerm.objects.all().order_by('term_en')
    topics = Topic.objects.filter(is_active=True)

    return render(request, 'pages/faq_glossary.html', {
        'faqs': faqs,
        'glossary_terms': glossary_terms,
        'topics': topics,
    })
