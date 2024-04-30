from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from .models import Basket
from moderno.models import Product
from moderno.utils import DataMixin


class BasketView(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'basket/basket.html'
    context_object_name = 'baskets'
    title_page = 'Корзина'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        baskets = Basket.objects.filter(user=self.request.user).select_related('user', 'product')
        total_sum = sum(basket.sum() for basket in baskets)
        context = super().get_context_data(**kwargs)
        context['total_sum'] = total_sum
        return self.get_mixin_context(context)


# def basket_add_remove(request, product_id):
#     user = request.user
#     current_page = request.META.get('HTTP_REFERER')
#     product = Product.published.get(id=product_id)
#     baskets = Basket.objects.filter(user=user, product=product)
#
#     if not baskets.exists():
#         Basket.objects.create(user=user, product=product, quantity=1)
#         return HttpResponseRedirect(current_page)
#     else:
#         return current_page, baskets


@login_required
def basket_add(request, product_id):
    user = request.user
    current_page = request.META.get('HTTP_REFERER')
    product = Product.published.get(id=product_id)
    baskets = Basket.objects.filter(user=user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    basket = baskets.first()
    basket.quantity += 1
    basket.save()
    return HttpResponseRedirect(current_page)


def basket_remove(request, product_id):
    user = request.user
    current_page = request.META.get('HTTP_REFERER')
    product = Product.published.get(id=product_id)
    baskets = Basket.objects.filter(user=user, product=product)

    basket = baskets.first()
    basket.quantity -= 1
    if basket.quantity == 0:
        return HttpResponseRedirect(current_page)
    basket.save()
    return HttpResponseRedirect(current_page)


def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
