# Generated by Django 3.2.3 on 2021-09-02 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_rename_watchlistitem_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='is_start',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
