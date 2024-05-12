from django.contrib.auth.models import AbstractUser
from django.db import models

from moderno.models import Product


class User(AbstractUser):
    class Genders(models.TextChoices):
        MALE = 'M', 'Мужчина'
        FEMALE = 'F', 'Женщина'
        UNDEFINED = 'U', 'Не выбран'

    image = models.ImageField(
        'Фотография',
        upload_to="users/%Y/%m/%d/",
        default='users/default.png',
        blank=True, null=True
    )

    date_birth = models.DateTimeField('Дата рождения', blank=True, null=True)
    gender = models.CharField(
        'Пол',
        max_length=1,
        choices=Genders.choices,
        default=Genders.UNDEFINED
    )

    def __str__(self):
        return self.username


