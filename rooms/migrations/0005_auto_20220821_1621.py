# Generated by Django 2.2.5 on 2022-08-21 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20220821_0008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='bedroomss',
            new_name='bedrooms',
        ),
    ]
