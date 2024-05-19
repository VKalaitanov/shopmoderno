from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse


class PublishedManager(models.Manager):
    """Менеджер опубликованных записей"""

    def get_queryset(self):
        return super().get_queryset().filter(available=True).select_related('category')


def product_image_directory_path(instance, filename):
    """Метод для сохранения фотографий по нужному пути"""
    if isinstance(instance, Product):
        return f'product_images/{instance.category.slug}/{instance.slug}/{filename}'
    return f'product_images/{instance.product.category.slug}/{instance.product.slug}/{filename}'


class Product(models.Model):
    name = models.CharField('Название товара', max_length=50, db_index=True)

    slug = models.SlugField(
        'Слаг',
        max_length=255,
        unique=True, db_index=True,
        validators=[
            MinLengthValidator(5, "Минимум 5 символов"),
            MaxLengthValidator(100, "Максимум 50 символов"),
        ])

    image = models.ImageField(
        'Фото товара',
        upload_to=product_image_directory_path,
        default='images/default.jpg',
        blank=True
    )

    description = models.TextField('Описание', blank=True)
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField('Время изменения', auto_now=True)
    price = models.FloatField('Цена', default=0)
    discount_price = models.FloatField('Цена со скидкой', blank=True, default=0, null=True)
    available = models.BooleanField('Наличие', default=True)

    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='product',
        verbose_name="Категории"
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-time_update',)
        indexes = [models.Index(fields=['name'])]  # ускоряет сортировку в таблице
        index_together = (('id', 'slug'),)  # индексируются вместе
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('moderno:product', kwargs={'product_slug': self.slug})

    def avg_rating(self):
        cache_key = f"product_avg_rating_{self.id}"
        cached_avg_rating = cache.get(cache_key)
        if cached_avg_rating is not None:
            return cached_avg_rating

        avg_rating = self.reviews.select_related('product', 'user') \
            .aggregate(Avg('rating'))['rating__avg']

        if avg_rating is not None:
            rounded_avg_rating = round(avg_rating, 1)
            cache.set(cache_key, rounded_avg_rating, timeout=20)
            return rounded_avg_rating

        return None

    def discount(self):
        if self.discount_price:
            return round((self.price - self.discount_price) / self.price * 100, 1)
        return None


class Size(models.Model):
    name = models.CharField('Размер', max_length=4)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sizes',
        verbose_name='Товар'
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name='sizes',
        verbose_name='Размер'
    )
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Размер для товара'
        verbose_name_plural = 'Размеры для товаров'

    def __str__(self):
        return f'{self.product}, размер:{self.size.name}, количество:{self.quantity}'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        default=None,
        on_delete=models.CASCADE,
        related_name='images'
    )

    images = models.FileField(upload_to=product_image_directory_path)

    def __str__(self):
        return self.product.name


class Category(models.Model):
    name = models.CharField('Название категории', max_length=100, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('moderno:category', kwargs={'category_slug': self.slug})


class Review(models.Model):
    class RatingChoice(models.IntegerChoices):
        one = 1, '★☆☆☆☆'
        two = 2, '★★☆☆☆'
        three = 3, '★★★☆☆'
        four = 4, '★★★★☆'
        five = 5, '★★★★★'

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Пользователь'
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Товар'
    )

    review = models.TextField('Отзыв', max_length=1000)
    time_create = models.DateTimeField('Дата добавления', auto_now_add=True)

    rating = models.IntegerField(
        'Оценка',
        blank=True,
        default=RatingChoice.five,
        null=True,
        choices=RatingChoice.choices
    )

    class Meta:
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create', 'rating'])]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Пользователь: {self.user}, товар: {self.product}, оценка: {self.rating}'


class Feedback(models.Model):
    """
    Модель обратной связи
    """
    subject = models.CharField('Тема письма', max_length=255)
    email = models.EmailField('Электронный адрес (email)', max_length=255)
    content = models.TextField('Содержимое письма', max_length=700)
    time_create = models.DateTimeField('Дата отправки', auto_now_add=True)

    ip_address = models.GenericIPAddressField(
        'IP отправителя',
        blank=True,
        null=True
    )

    user = models.ForeignKey(
        get_user_model(),
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-time_create']
        db_table = 'app_feedback'

    def __str__(self):
        return f'Вам письмо от {self.user.name}, email: {self.email}'
