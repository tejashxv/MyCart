# Generated by Django 5.1.3 on 2025-01-06 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='state',
            field=models.CharField(default='', max_length=100),
        ),
    ]