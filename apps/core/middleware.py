class LanguageMiddleware:
    """
    Middleware to handle language switching ('gu' default, 'en')
    and accessibility theme switching ('light', 'dark', 'contrast').
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Language handling (gu is strict default)
        lang = request.GET.get('lang')
        if lang in ['gu', 'en']:
            request.session['site_lang'] = lang
        elif 'site_lang' not in request.session:
            request.session['site_lang'] = 'gu'

        # Theme handling
        theme = request.GET.get('theme')
        if theme in ['light', 'dark', 'contrast']:
            request.session['site_theme'] = theme

        request.site_lang = request.session.get('site_lang', 'gu')
        request.site_theme = request.session.get('site_theme', 'light')
        response = self.get_response(request)
        return response

