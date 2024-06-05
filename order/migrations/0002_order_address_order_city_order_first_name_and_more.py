# Generated by Django 4.2.5 on 2024-05-22 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=250, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=100, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(max_length=20, null=True, verbose_name='Почтовый индекс'),
        ),
    ]
