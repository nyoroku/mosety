from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from .models import Redirect


class SEORedirectMiddleware:
    """
    Checks if the incoming request path matches an active SEO Redirect entry.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        # Check exact path or path with trailing slash
        redirect_obj = Redirect.objects.filter(is_active=True, old_path=path).first()
        if not redirect_obj and not path.endswith('/'):
            redirect_obj = Redirect.objects.filter(is_active=True, old_path=f"{path}/").first()

        if redirect_obj:
            if redirect_obj.status_code == 301:
                return HttpResponsePermanentRedirect(redirect_obj.new_path)
            return HttpResponseRedirect(redirect_obj.new_path)

        return self.get_response(request)
