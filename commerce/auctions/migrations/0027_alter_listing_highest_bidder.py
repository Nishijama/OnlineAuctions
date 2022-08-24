# Generated by Django 4.0.6 on 2022-08-21 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_listing_highest_bidder_alter_listing_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='highest_bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='placed_bids', to=settings.AUTH_USER_MODEL),
        ),
    ]