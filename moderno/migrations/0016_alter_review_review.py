# Generated by Django 5.0.2 on 2024-04-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderno', '0015_alter_review_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(blank=True, default=5, null=True, verbose_name='Отзыв'),
        ),
    ]
