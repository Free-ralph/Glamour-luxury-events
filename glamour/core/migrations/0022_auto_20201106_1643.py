# Generated by Django 3.1.2 on 2020-11-06 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_addons_giftbox_giftitem_trays'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='giftbox',
            options={'verbose_name_plural': 'GiftBoxes'},
        ),
        migrations.RemoveField(
            model_name='giftbox',
            name='GiftItem',
        ),
        migrations.DeleteModel(
            name='GiftItem',
        ),
    ]
