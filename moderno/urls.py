from django.urls import path

from . import views
from .views import ProductSearchResultView

app_name = 'moderno'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.FeedbackCreateView.as_view(), name='contacts'),
    path('category/<slug:category_slug>/', views.ProductCategory.as_view(), name='category'),
    path('product/<slug:product_slug>/', views.ShowProduct.as_view(), name='product'),
    path('search/', ProductSearchResultView.as_view(), name='search'),

]
