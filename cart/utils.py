from decimal import Decimal

from django.db.models import F
from django.shortcuts import get_object_or_404
from cart.models import Cart
from moderno.models import ProductSize


def get_cart_items(user):
    return Cart.objects.filter(user=user).select_related('user', 'product')


def calculate_total_price(cart_items):
    return sum(Decimal(item.sum()) for item in cart_items)


def calculate_total_discount_price(cart_items):
    return sum(
        (Decimal(item.product.discount_price or item.product.price)) * item.quantity
        for item in cart_items
    )


def update_product_quantity(cart_item, quantity_delta):
    product_size = get_object_or_404(
        ProductSize,
        product=cart_item.product,
        size__name=cart_item.size
    )
    product_size.quantity = F('quantity') + quantity_delta
    product_size.save()
