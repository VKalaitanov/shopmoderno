from django.core.cache import cache

from cart.models import Cart
from like.models import Like
from shopmoderno import settings
from .models import Category, Product


def get_info_context(request):
    # cached_data = cache.get('info_context_data')
    # if cached_data:
    #     return cached_data
    user = request.user.id
    cart = Cart.objects.select_related('user', 'product').filter(user=user)
    cart_items = cart.count()
    cart_items_quantity = sum(item.quantity for item in cart)

    likes = Like.objects.select_related('user', 'product').filter(user=user)
    quantity_likes = likes.count()

    data = {
        'category': Category.objects.all(),
        'cart_items': cart_items,
        'cart_items_quantity': cart_items_quantity,
        'quantity_likes': quantity_likes,
        'RECAPTCHA_KEY': settings.RECAPTCHA_KEY,
    }

    # cache.set('info_context_data', data, timeout=2)  # Кэшируем на 1 час
    return data

# def get_info_context(request):
#     cart = Cart.objects.select_related('user', 'product').filter(user=request.user.id)
#     cart_items = cart.count()
#     cart_items_quantity = sum(item.quantity for item in cart)
#
#     likes = Like.objects.select_related('user', 'product').filter(user=request.user.id)
#     quantity_likes = likes.count()
#     data = {
#         'category': Category.objects.all(),
#         'cart_items': cart_items,
#         'cart_items_quantity': cart_items_quantity,
#         'quantity_likes': quantity_likes,
#     }
#
#     return data
