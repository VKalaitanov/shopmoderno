from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView

from cart.forms import AddToCartForm
from .forms import ReviewForm, FeedbackCreateForm
from .email import send_contact_email_message
from .models import Product, ProductImage, Feedback
from .utils import DataMixin, get_client_ip
from .tasks import send_contact_email_message_task


class HomePage(DataMixin, ListView):
    template_name = 'moderno/index.html'
    context_object_name = 'products'
    title_page = 'Главная страница'

    def get_queryset(self):
        return Product.published.all().select_related('category').prefetch_related('likes')


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
        error_message = self.request.session.pop('error_message', None)
        images = (
            ProductImage.objects
            .filter(product=product)
            .select_related('product', )
        )

        reviews = (
            product.reviews.all()
            .order_by('-time_create')
            .select_related('user', 'product')
        )

        return self.get_mixin_context(
            context,
            title=context['product'].name,
            images=images,
            cart_product_form=self.cart_product_form,
            error_message=error_message,
            reviews=reviews,
        )

    def get_object(self, queryset=None):
        slug = self.kwargs[self.slug_url_kwarg]
        return get_object_or_404(Product.published, slug=slug)


def about(request):
    return render(request, 'moderno/about.html', {'title': 'Страница про нас'})


class FeedbackCreateView(SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = 'Ваше письмо успешно отправлено администрации сайта'
    template_name = 'moderno/contacts.html'
    extra_context = {'title': 'Страница контакты'}
    success_url = reverse_lazy('moderno:contacts')

    def form_valid(self, form):
        # if form.is_valid():
        #     feedback = form.save(commit=False)
        #     feedback.ip_address = get_client_ip(self.request)
        #     if self.request.user.is_authenticated:
        #         feedback.user = self.request.user
        #
        #     send_contact_email_message(
        #         feedback.subject, feedback.email, feedback.content,
        #         feedback.ip_address, feedback.user_id
        #     )
        # return super().form_valid(form)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = get_client_ip(self.request)
            if self.request.user.is_authenticated:
                feedback.user = self.request.user

            send_contact_email_message_task.delay(
                feedback.subject, feedback.email,
                feedback.content, feedback.ip_address, feedback.user_id
            )
        return super().form_valid(form)


class ProductSearchResultView(ListView):
    """
    Реализация поиска статей на сайте
    """
    model = Product
    context_object_name = 'products'
    # paginate_by = 2
    allow_empty = True
    template_name = 'moderno/index.html'

    def get_queryset(self):
        query = self.request.GET.get('do')
        search_vector = SearchVector('description', weight='B') + SearchVector('name', weight='A')
        search_query = SearchQuery(query)
        queryset = (
            self.model.published.annotate(
                rank=SearchRank(search_vector, search_query)) \
                .filter(rank__gte=0.3).order_by('-rank')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Результаты поиска: {self.request.GET.get("do")}'
        return context
        # context = super().get_context_data(**kwargs)
        # query = self.request.GET.get('do')
        # if query:
        #     context['title'] = f'Результаты поиска: {self.object_list.count()}'
        # else:
        #     context['title'] = 'Результаты поиска'
        # context['total_results'] = self.object_list.count()  # Общее количество результатов
        # return context
