# Generated by Django 3.1.2 on 2020-11-06 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20201105_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='sizes',
        ),
    ]
