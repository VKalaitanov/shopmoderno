from django.urls import path

from . import views

app_name = "basket"

urlpatterns = [
    path('basket/', views.BasketView.as_view(), name='basket'),
    path('basket-add/<int:product_id>', views.basket_add, name='basket_add'),
    path('basket-remove/<int:product_id>', views.basket_remove, name='basket_remove'),
    path('basket-delete/<int:id>', views.basket_delete, name='basket_delete'),
]
