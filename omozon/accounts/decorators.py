from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def login_required_custom_user():
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_custom_user:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator