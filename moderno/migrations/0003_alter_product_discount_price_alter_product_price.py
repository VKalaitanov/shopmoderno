# Generated by Django 4.2.5 on 2024-05-22 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderno', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Цена со скидкой'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Цена'),
        ),
    ]
