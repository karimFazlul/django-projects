# Generated by Django 3.1.6 on 2021-06-12 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='catalog.Category'),
        ),
    ]
