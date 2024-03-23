# Generated by Django 4.2.5 on 2024-03-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0022_shippingcharge'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shippingcharge',
            field=models.DecimalField(decimal_places=2, default=350, max_digits=10),
            preserve_default=False,
        ),
    ]
