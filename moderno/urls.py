from django.urls import path

from . import views

app_name = "moderno"

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('category/<slug:category_slug>/', views.ProductCategory.as_view(), name='category'),
    path('product/<slug:product_slug>/', views.ShowProduct.as_view(), name='product'),
]
