# Generated by Django 4.1.4 on 2022-12-12 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='blog/static/assets/img/posts/thumbnails'),
        ),
    ]
