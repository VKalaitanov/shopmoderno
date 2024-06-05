from django.db import models
from users.models import User
from moderno.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='orders'
    )
    first_name = models.CharField('Имя', max_length=50, null=True)
    last_name = models.CharField('Фамилия', max_length=50, null=True)
    phone = models.CharField('Телефон', max_length=20, null=True)
    address = models.CharField('Адрес', max_length=250, null=True)
    postal_code = models.CharField('Почтовый индекс', max_length=20, null=True)
    city = models.CharField('Город', max_length=100, null=True)
    created_timestamp = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated_timestamp = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    total_price = models.IntegerField('Общая стоимость')
    is_paid = models.BooleanField('Оплачено', default=False)

    class Meta:
        ordering = ('-created_timestamp',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id} от {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    size = models.CharField(max_length=4, verbose_name='Размер')
    price = models.IntegerField('Цена')

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.product.name} ({self.size}) - {self.quantity} шт.'
