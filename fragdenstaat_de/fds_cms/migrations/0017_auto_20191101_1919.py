# Generated by Django 2.2.4 on 2019-11-01 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fds_cms', '0016_svgimagecmsplugin'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentembedcmsplugin',
            name='page_number',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='documentembedcmsplugin',
            name='settings',
            field=models.TextField(default='{}'),
        ),
    ]
