from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse


def user_is_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(_, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect(reverse('login') + f"?next={request.path}")

        return view_func(_, request, *args, **kwargs)

    return _wrapped_view
