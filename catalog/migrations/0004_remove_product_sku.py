# Generated by Django 3.1.6 on 2021-06-12 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210612_0318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
    ]