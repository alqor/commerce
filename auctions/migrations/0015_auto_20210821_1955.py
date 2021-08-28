# Generated by Django 3.2.3 on 2021-08-21 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_bid_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='start_bid',
        ),
        migrations.AlterField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listing'),
        ),
    ]
