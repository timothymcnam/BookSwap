# Generated by Django 2.0.2 on 2018-03-25 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BookSwap', '0008_auto_20180325_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='isbn',
        ),
    ]
