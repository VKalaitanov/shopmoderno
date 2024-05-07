from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart-add/<int:product_id>', views.cart_add, name='cart_add'),
    # path('cart-remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart-delete/<int:id>', views.cart_delete, name='cart_delete'),
]
