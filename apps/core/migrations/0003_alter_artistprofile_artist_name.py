# Generated by Django 5.1.7 on 2025-03-21 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_music_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistprofile',
            name='artist_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
