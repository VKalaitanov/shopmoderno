# Generated by Django 4.2.5 on 2024-05-21 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('moderno', '0001_initial'),
        ('like', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='moderno.product', verbose_name='Товар'),
        ),
    ]
