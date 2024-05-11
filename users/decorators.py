from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def redirect_authenticated_users(redirect_to):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.path == reverse_lazy(redirect_to):
                return HttpResponseRedirect(reverse_lazy('users:profile'))
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator
