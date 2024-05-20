from django.contrib.auth import get_user_model
from django.db import models

from moderno.models import Product


class Like(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='likes'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='likes'
    )
    like = models.BooleanField(default=False, verbose_name='Избранное')
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления лайка'
    )

    class Meta:
        ordering = ('-created_timestamp',)
        unique_together = ('user', 'product')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные товары'

    def __str__(self):
        return f'Избранное для: {self.user.username} | Продукт: {self.product.name}'


get_user_model().add_to_class('favorites', models.ManyToManyField(Product, through=Like, related_name='liked_by'))
