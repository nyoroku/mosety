class UTMMiddleware:
    """
    Captures marketing attribution parameters on the first landing page and persists
    them in request.session for attribution upon booking lead creation.
    """
    UTM_FIELDS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        has_utm = any(field in request.GET for field in self.UTM_FIELDS)
        if has_utm:
            utm_data = request.session.get('utm_data', {})
            for field in self.UTM_FIELDS:
                val = request.GET.get(field)
                if val:
                    utm_data[field] = val[:100]

            if 'landing_page' not in utm_data:
                utm_data['landing_page'] = request.build_absolute_uri()[:255]
            if 'referrer' not in utm_data:
                utm_data['referrer'] = request.META.get('HTTP_REFERER', '')[:255]

            request.session['utm_data'] = utm_data
            if hasattr(request.session, 'modified'):
                request.session.modified = True

        return self.get_response(request)

