# Generated by Django 4.2.5 on 2024-03-20 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0017_offer_order_discounted_price_order_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='code',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
