# Generated by Django 3.2.5 on 2021-07-13 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_remove_category_sub_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='sub_Categories',
            field=models.TextField(default=''),
        ),
    ]