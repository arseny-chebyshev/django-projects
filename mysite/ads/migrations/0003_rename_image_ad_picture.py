# Generated by Django 3.2.5 on 2022-01-31 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_auto_20220131_1832'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ad',
            old_name='image',
            new_name='picture',
        ),
    ]
