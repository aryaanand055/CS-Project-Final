# Generated by Django 4.2.5 on 2023-11-20 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_brand_remove_products_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.brand'),
        ),
    ]