# Generated by Django 3.2.3 on 2021-08-11 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]