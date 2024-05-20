from django.db import models

from moderno.models import Product
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='cart'
    )

    size = models.CharField('Размер', max_length=4)

    quantity = models.PositiveIntegerField(
        'Количество',
        default=0
    )

    created_timestamp = models.DateTimeField(
        'Дата добавления товара',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-created_timestamp',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина для: {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price
