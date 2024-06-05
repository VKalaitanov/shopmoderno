from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from moderno.models import Product, ProductSize
from moderno.utils import DataMixin
from .forms import AddToCartForm
from .models import Cart
from .utils import update_product_quantity, calculate_total_discount_price, calculate_total_price, get_cart_items


class CartView(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'cart'
    title_page = 'Корзина'

    def get_cart(self):
        return get_cart_items(self.request.user)

    def get_queryset(self):
        return self.get_cart()

    def get_total_price(self, cart):
        return calculate_total_price(cart)

    def get_total_discount_price(self, cart):
        return calculate_total_discount_price(cart)

    def get_context_data(self, **kwargs):
        cart = self.get_cart()
        context = super().get_context_data(**kwargs)
        context['total_price'] = self.get_total_price(cart)
        context['total_discount_price'] = self.get_total_discount_price(cart)
        context['discount'] = context['total_price'] - context['total_discount_price']
        return self.get_mixin_context(context)


@login_required
def cart_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AddToCartForm(request.POST, product_id=product_id)
        if form.is_valid():
            user = request.user
            product = get_object_or_404(Product, id=product_id)
            quantity = form.cleaned_data['quantity']
            size = form.cleaned_data['size']
            product_size = ProductSize.objects.filter(
                product=product, size=size
            ).first()

            if product_size and product_size.quantity >= quantity:
                Cart.objects.create(
                    user=user, product=product,
                    quantity=quantity, size=size.name
                )
                update_product_quantity(product_size, -quantity)
                return HttpResponseRedirect(current_page)

            else:
                error_message = (
                    'Товар с выбранным размером недоступен'
                    ' или количество товара слишком мало.'
                )
                request.session['error_message'] = error_message
    else:
        form = AddToCartForm(product_id=product_id)
    return HttpResponseRedirect(current_page)


@login_required
def cart_delete(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    update_product_quantity(cart_item, cart_item.quantity)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
