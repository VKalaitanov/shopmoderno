# Generated by Django 4.2.5 on 2024-05-19 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderno', '0004_alter_review_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Отзыв'),
        ),
    ]
