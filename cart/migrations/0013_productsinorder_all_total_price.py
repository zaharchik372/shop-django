# Generated by Django 3.2.20 on 2024-05-28 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_auto_20240527_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsinorder',
            name='all_total_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Общая итоговая цена'),
        ),
    ]
