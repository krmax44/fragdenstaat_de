# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-23 12:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0020_old_tree_cleanup'),
        ('document', '0006_auto_20180522_0114'),
        ('fds_cms', '0005_foirequestlistcmsplugin'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentEmbedCMSPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='fds_cms_documentembedcmsplugin', serialize=False, to='cms.CMSPlugin')),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='document.Document')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]