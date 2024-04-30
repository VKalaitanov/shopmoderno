from django.contrib.auth import get_user_model
from django.db import models

from moderno.models import Product


class Like(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='like'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='like'
    )
    like = models.PositiveIntegerField(default=0, verbose_name='Лайк')
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления лайка'
    )

    class Meta:
        ordering = ('-created_timestamp',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные товары'

    def __str__(self):
        return f'Избранное для: {self.user.username} | Продукт: {self.product.name}'
