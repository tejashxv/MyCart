# Generated by Django 5.1.4 on 2025-01-24 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_userextra_location_userextra_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextra',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userextra',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userextra',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userextra',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
