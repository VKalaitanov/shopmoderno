from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class RedirectIfAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == reverse_lazy('users:register'):
            return HttpResponseRedirect(reverse_lazy('users:profile'))
        response = self.get_response(request)
        return response
