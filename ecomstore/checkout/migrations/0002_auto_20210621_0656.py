# Generated by Django 3.1.6 on 2021-06-21 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='billing_address_1',
            new_name='shipping_name_first',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='billing_city',
            new_name='shipping_name_last',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_address_2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_state',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_zip',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_name',
        ),
    ]
