# Generated by Django 4.2.5 on 2023-10-14 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='tagline',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
