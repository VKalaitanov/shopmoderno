from basket.models import Basket
from like.models import Like
from .models import Category


def get_info_context(request):
    baskets = Basket.objects.filter(user=request.user.id)
    total_quantity = sum(basket.quantity for basket in baskets)
    likes = Like.objects.filter(user=request.user.id)
    quantity_likes = sum(like.like for like in likes)

    data = {
        'category': Category.objects.all(),
        'total_quantity': total_quantity,
        'quantity_likes': quantity_likes,
    }

    return data
