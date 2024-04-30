from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from moderno.models import Product
from .models import Like
from moderno.utils import DataMixin


class LikeView(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'like/like.html'
    context_object_name = 'likes'
    title_page = 'Избранные товары'

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related('user', 'product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


@login_required
def like_add(request, product_id):
    user = request.user
    current_page = request.META.get('HTTP_REFERER')
    product = Product.published.get(id=product_id)
    likes = Like.objects.filter(user=user, product=product)

    if not likes.exists():
        Like.objects.create(user=user, product=product, like=1)
        return HttpResponseRedirect(current_page)
    like = likes.first()
    like.delete()
    return HttpResponseRedirect(current_page)
