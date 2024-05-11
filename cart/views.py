from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from moderno.models import Product, ProductSize
from moderno.utils import DataMixin
from .forms import AddToCartForm
from .models import Cart


class CartView(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'cart'
    title_page = 'Корзина'

    def get_cart(self):
        cart = Cart.objects.filter(user=self.request.user)
        return cart.select_related('user', 'product')

    def get_queryset(self):
        return self.get_cart()

    def get_total_price(self, cart):
        total_price = sum(Decimal(item.sum()) for item in cart)
        return round(total_price, 2)

    def get_total_discount_price(self, cart):
        summ = 0
        for item in cart:
            if item.product.discount_price:
                summ += Decimal(item.product.discount_price) * item.quantity
            else:
                summ += Decimal(item.product.price) * item.quantity
        return round(summ, 2)

    def get_context_data(self, **kwargs):
        cart = self.get_cart()
        context = super().get_context_data(**kwargs)
        context['total_sum'] = self.get_total_price(cart)
        context['total_discount_price'] = self.get_total_discount_price(cart)
        context['discount'] = context['total_sum'] - context['total_discount_price']
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
    # quantity = int(request.POST.get('quantity', 1))
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            user = request.user
            product = Product.published.get(id=product_id)
            quantity = form.cleaned_data['quantity']
            size = form.cleaned_data['size']
            product_size = ProductSize.objects.filter(product=product, size=size).first()
            if product_size and product_size.quantity >= quantity:
                Cart.objects.create(user=user, product=product, quantity=quantity, size=size)
                return HttpResponseRedirect(current_page)
            else:
                error_message = 'Товар с выбранным размером недоступен или количество товара слишком мало.'
                request.session['error_message'] = error_message
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
