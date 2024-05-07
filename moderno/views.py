from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from cart.forms import AddToCartForm
from .forms import ReviewForm
from .models import Product, ProductImage
from .utils import DataMixin


class HomePage(DataMixin, ListView):
    template_name = 'moderno/index.html'
    context_object_name = 'products'
    title_page = 'Главная страница'

    def get_queryset(self):
        return Product.published.all().select_related('category', )


class ProductCategory(DataMixin, ListView):
    context_object_name = 'products'
    allow_empty = False
    template_name = 'moderno/index.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = Product.published.filter(category__slug=category_slug)
        return category.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['products'][0].category

        mixin_context = self.get_mixin_context(
            context,
            title='Категория: ' + category.name,
        )

        return mixin_context


class ShowProduct(DataMixin, FormMixin, DetailView):
    template_name = 'moderno/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    form_class = ReviewForm
    cart_product_form = AddToCartForm()

    def get_success_url(self, **kwargs):
        product_slug = self.get_object().slug
        return reverse_lazy('moderno:product', kwargs={'product_slug': product_slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.review = form.save(commit=False)
        self.review.user = self.request.user
        self.review.product = self.get_object()
        self.review.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs[self.slug_url_kwarg]
        product = get_object_or_404(Product, slug=slug)
        images = (
            ProductImage.objects
            .filter(product=product)
            .select_related('product', )
        )

        return self.get_mixin_context(
            context,
            title=context['product'].name,
            images=images,
            cart_product_form=self.cart_product_form
        )

    def get_object(self, queryset=None):
        slug = self.kwargs[self.slug_url_kwarg]
        return get_object_or_404(Product.published, slug=slug)


def about(request):
    return render(request, 'moderno/about.html', {'title': 'Страница про нас'})


def contacts(request):
    return render(request, 'moderno/contacts.html', {'title': 'Страница контакты'})
