# Generated by Django 5.0.2 on 2024-05-06 12:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('like', '0001_initial'),
        ('moderno', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='moderno.product', verbose_name='Товар'),
        ),
    ]
