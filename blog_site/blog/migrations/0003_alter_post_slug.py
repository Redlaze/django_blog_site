# Generated by Django 5.0.4 on 2025-07-27 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_options_alter_post_author_alter_post_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, unique_for_date='publish'),
        ),
    ]
