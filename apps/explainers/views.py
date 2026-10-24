from django.shortcuts import render, get_object_or_404
from .models import Explainer
from apps.topics.models import Topic


def explainers_list(request):
    """List of plain-language legal explainers with topic filter."""
    topic_slug = request.GET.get('topic')
    topics = Topic.objects.filter(is_active=True)
    
    explainers = Explainer.objects.filter(editorial_status='PUBLISHED')
    if topic_slug:
        explainers = explainers.filter(topic__slug=topic_slug)
        
    return render(request, 'pages/explainers_list.html', {
        'explainers': explainers,
        'topics': topics,
        'selected_topic_slug': topic_slug,
    })


def explainer_detail(request, slug):
    """
    Editorial Explainer Reading Page (Image 3 design reference):
    Calm reading column, clear title/deck, reviewer/author metadata,
    section headings, statutory callouts, source citations, last verified date,
    and visible non-advice disclaimer.
    """
    explainer = get_object_or_404(Explainer, slug=slug, editorial_status='PUBLISHED')
    related_explainers = Explainer.objects.filter(
        topic=explainer.topic, 
        editorial_status='PUBLISHED'
    ).exclude(id=explainer.id)[:3]

    # Increment view counter
    explainer.views_count += 1
    explainer.save(update_fields=['views_count'])

    return render(request, 'pages/explainer_detail.html', {
        'explainer': explainer,
        'related_explainers': related_explainers,
    })
