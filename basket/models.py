from django.db import models

from moderno.models import Product
from users.models import User


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='basket'
                             )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='basket'
                                )
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления товара')

    class Meta:
        ordering = ('-created_timestamp',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина для: {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price
