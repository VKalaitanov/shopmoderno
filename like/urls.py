from django.urls import path

from . import views

app_name = 'like'

urlpatterns = [
    path('like/', views.LikeView.as_view(), name='like'),
    path('like/<int:product_id>', views.like_add, name='like_add'),
]