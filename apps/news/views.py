from django.shortcuts import render, get_object_or_404
from .models import NewsArticle, NewsCategory


def news_list(request):
    """News and updates feed with category filtering."""
    cat = request.GET.get('category')
    articles = NewsArticle.objects.filter(editorial_status='PUBLISHED')
    if cat:
        articles = articles.filter(category=cat)
        
    return render(request, 'pages/news_list.html', {
        'articles': articles,
        'categories': NewsCategory.choices,
        'selected_category': cat,
    })


def news_detail(request, slug):
    """Editorial news article page with verified source list and fact-check provenance."""
    article = get_object_or_404(NewsArticle, slug=slug, editorial_status='PUBLISHED')
    related_articles = NewsArticle.objects.filter(
        category=article.category, 
        editorial_status='PUBLISHED'
    ).exclude(id=article.id)[:3]
    
    return render(request, 'pages/news_detail.html', {
        'article': article,
        'related_articles': related_articles,
    })
