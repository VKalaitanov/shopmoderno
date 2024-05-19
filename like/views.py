from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from moderno.models import Product
from moderno.utils import DataMixin
from .models import Like


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
    print(f'Получен запрос для продукта ID: {product_id}')  # Отладочное сообщение
    product = get_object_or_404(Product, id=product_id)
    like, created = Like.objects.get_or_create(user=request.user, product=product)

    if not created:
        print('Like уже существует, удаляем его.')  # Отладочное сообщение
        like.delete()
        liked = False
    else:
        print('Создаем новый Like.')  # Отладочное сообщение
        liked = True

    print(f'Ответ: liked = {liked}')  # Отладочное сообщение
    return JsonResponse({'liked': liked})
    # return redirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(current_page)


