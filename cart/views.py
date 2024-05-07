from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from moderno.models import Product
from moderno.utils import DataMixin
from .forms import AddToCartForm
from .models import Cart


class CartView(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'cart'
    title_page = 'Корзина'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        cart = Cart.objects.filter(user=self.request.user).select_related('user', 'product')
        total_sum = sum(item.sum() for item in cart)
        context = super().get_context_data(**kwargs)
        context['total_sum'] = total_sum
        return self.get_mixin_context(context)


# @login_required
# def cart_add(request, product_id):
#     user = request.user
#     current_page = request.META.get('HTTP_REFERER')
#     product = Product.published.get(id=product_id)
#     carts = Cart.objects.filter(user=user, product=product)
#     quantity = int(request.POST.get('quantity', 1))
#
#     if not carts.exists():
#         Cart.objects.create(user=user, product=product, quantity=quantity)
#         return HttpResponseRedirect(current_page)
#     cart = carts.first()
#     cart.quantity += quantity
#     cart.save()
#     return HttpResponseRedirect(current_page)


@login_required
def cart_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')

    # product = Product.published.get(id=product_id)
    # carts = Cart.objects.filter(user=user, product=product)
    # quantity = int(request.POST.get('quantity', 1))

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # Обработка добавления товара в корзину
            user = request.user
            product = Product.published.get(id=product_id)
            quantity = form.cleaned_data['quantity']
            size = form.cleaned_data['size']

            # if not carts.exists():
            Cart.objects.create(user=user, product=product, quantity=quantity, size=size)
            return HttpResponseRedirect(current_page)
    # Для добавляения количества товара в корзину
    # cart = carts.first()
    # cart.quantity += quantity
    # cart.save()
    return HttpResponseRedirect(current_page)

# Для уменьшения количества товара в корзине
# def cart_remove(request, product_id):
#     user = request.user
#     current_page = request.META.get('HTTP_REFERER')
#     product = Product.published.get(id=product_id)
#     carts = Cart.objects.filter(user=user, product=product)
#
#     cart = carts.first()
#     cart.quantity -= 1
#     if cart.quantity == 0:
#         return HttpResponseRedirect(current_page)
#     cart.save()
#     return HttpResponseRedirect(current_page)


def cart_delete(request, id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
