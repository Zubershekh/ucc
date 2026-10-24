from django.shortcuts import render
from .models import TimelineEvent, TimelineCategory


def timeline_page(request):
    """
    Legislative & Implementation Timeline:
    Dated events with verified source links and the 8-state status taxonomy.
    """
    category_filter = request.GET.get('category')
    events = TimelineEvent.objects.all().order_by('-event_date')
    
    if category_filter:
        events = events.filter(category=category_filter)
        
    return render(request, 'pages/timeline.html', {
        'events': events,
        'categories': TimelineCategory.choices,
        'selected_category': category_filter,
    })
