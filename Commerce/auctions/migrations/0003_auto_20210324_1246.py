# Generated by Django 3.1.7 on 2021-03-24 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_winners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid_categories',
            field=models.ManyToManyField(related_name='tag', to='auctions.Category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bid_comments',
            field=models.ManyToManyField(blank=True, related_name='comments', to='auctions.Comments'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bid_image',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_bidder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to='auctions.bidder'),
        ),
    ]
