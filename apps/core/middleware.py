class LanguageMiddleware:
    """
    Middleware to handle language switching between Gujarati ('gu') and English ('en').
    Respects ?lang= parameter and persists choice in user session.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get('lang')
        if lang in ['gu', 'en']:
            request.session['site_lang'] = lang
        elif 'site_lang' not in request.session:
            # Default to Gujarati primary content as requested by user, with English UI support
            request.session['site_lang'] = 'gu'

        request.site_lang = request.session.get('site_lang', 'gu')
        response = self.get_response(request)
        return response
