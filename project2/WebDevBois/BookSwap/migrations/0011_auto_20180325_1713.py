# Generated by Django 2.0.2 on 2018-03-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookSwap', '0010_auto_20180325_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='university',
            field=models.CharField(blank=True, choices=[('University of Massachusetts Amherst', 'University of Massachusetts Amherst'), ('Hampshire College', 'Hampshire College'), ('Smith College', 'Smith College'), ('Mount Holyoke College', 'Mount Holyoke College'), ('Amherst College', 'Amherst College'), ('Other', 'Other'), ('None', 'None')], default='None', help_text='School or University', max_length=200),
        ),
    ]
