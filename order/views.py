from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from cart.utils import get_cart_items, calculate_total_discount_price
from .forms import OrderCreateForm
from .models import OrderItem, Order


@login_required
def order_create(request):
    cart_items = get_cart_items(request.user)
    total_price = calculate_total_discount_price(cart_items)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    size=item.size,
                    price=item.product.discount_price \
                        if item.product.discount_price \
                        else item.product.price
                )
                item.delete()
            return redirect('order:order_success', order.id)
    else:
        form = OrderCreateForm()

    return render(
        request, 'order/order_create.html',
        {
            'form': form,
            'cart_items': cart_items,
            'total_price': total_price,
        }
    )


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(
        request,
        'order/order_success.html',
        {'order': order}
    )
