from django.shortcuts import render, get_object_or_404
from .models import Topic


def topics_list(request):
    """List all 6 Core UCC Subject Categories."""
    topics = Topic.objects.filter(is_active=True).order_by('order')
    return render(request, 'pages/topics_list.html', {'topics': topics})


def topic_detail(request, slug):
    """Topic Detail: Overview, statutory provisions, explainers, FAQs."""
    topic = get_object_or_404(Topic, slug=slug, is_active=True)
    explainers = topic.explainers.filter(editorial_status='PUBLISHED')
    faqs = topic.faqs.filter(is_published=True)
    
    return render(request, 'pages/topic_detail.html', {
        'topic': topic,
        'explainers': explainers,
        'faqs': faqs,
    })
