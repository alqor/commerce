# Generated by Django 3.2.3 on 2021-08-29 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20210821_1955'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WatchlistItem',
            new_name='Watchlist',
        ),
    ]