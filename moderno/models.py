from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse


class PublishedManager(models.Manager):
    """Менеджер опубликованных записей"""

    def get_queryset(self):
        return super().get_queryset().filter(available=True)


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
        'Фото',
        upload_to=product_image_directory_path,
        default='images/default.jpg',
        blank=True
    )

    description = models.TextField('Описание', blank=True)
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField('Время изменения', auto_now=True)
    price = models.FloatField('Цена', default=0)
    discount_price = models.FloatField('Цена со скидкой', blank=True, default=0, null=True)
    # sizes = models.ManyToManyField('ProductSize', related_name='size', blank=True)
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
        # if hasattr(self, 'avg_rating'):
        #     print(self.avg_rating)
        #     return self.avg_rating

        avg_rating = self.review.select_related('product', 'user').aggregate(Avg('rating'))
        if avg_rating['rating__avg'] is not None:
            return round(avg_rating['rating__avg'], 1)
        return None

    def discount(self):
        if self.discount_price:
            return round((self.price - self.discount_price) / self.price * 100, 2)
        return None


class Size(models.Model):
    size = models.CharField('Размер', max_length=4)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.size


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='sizes')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Размер для товара'
        verbose_name_plural = 'Размеры для товаров'

    def __str__(self):
        return f'Товар: {self.product}, размер: {self.size}, количество: {self.quantity}'


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
        related_name='review', verbose_name='Пользователь'
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='review', verbose_name='Товар'
    )

    review = models.TextField('Отзыв', max_length=1000, blank=True, null=True)
    create_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    rating = models.IntegerField(
        'Оценка',
        blank=True,
        default=RatingChoice.five,
        null=True,
        choices=RatingChoice.choices
    )

    class Meta:
        ordering = ('-create_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Пользователь: {self.user}, товар: {self.product}, оценка: {self.rating}'
