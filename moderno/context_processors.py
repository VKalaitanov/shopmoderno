from cart.models import Cart
from like.models import Like
from .models import Category


def get_info_context(request):
    cart = Cart.objects.filter(user=request.user.id).select_related('user', 'product')
    cart_items = cart.count()
    cart_items_quantity = sum(item.quantity for item in cart)

    likes = Like.objects.filter(user=request.user.id).select_related('user', 'product')
    quantity_likes = likes.count()

    data = {
        'category': Category.objects.all(),
        'cart_items': cart_items,
        'cart_items_quantity': cart_items_quantity,
        'quantity_likes': quantity_likes,
        'like': likes,
    }

    return data
