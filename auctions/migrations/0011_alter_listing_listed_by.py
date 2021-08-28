# Generated by Django 3.2.3 on 2021-08-12 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_listed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='listed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_items', to=settings.AUTH_USER_MODEL),
        ),
    ]