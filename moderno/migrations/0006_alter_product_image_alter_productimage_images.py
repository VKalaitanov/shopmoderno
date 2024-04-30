# Generated by Django 5.0.2 on 2024-04-27 11:12

import moderno.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderno', '0005_remove_review_changes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='/media/product_images/default.png', upload_to=moderno.models.product_image_directory_path, verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='images',
            field=models.FileField(upload_to=moderno.models.product_image_directory_path),
        ),
    ]
