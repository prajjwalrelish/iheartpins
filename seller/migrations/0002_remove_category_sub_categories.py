# Generated by Django 3.2.5 on 2021-07-13 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='sub_Categories',
        ),
    ]
