# Generated by Django 5.1.7 on 2025-03-18 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistprofile',
            name='first_name',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artistprofile',
            name='last_name',
            field=models.CharField(default=3, max_length=200),
            preserve_default=False,
        ),
    ]
