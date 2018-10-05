# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-23 11:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('cms', '0020_old_tree_cleanup'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publicbody', '0021_proposedpublicbody'),
        ('foirequest', '0026_deliverystatus_retry_count'),
        ('fds_cms', '0004_primarylinkcmsplugin'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoiRequestListCMSPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='fds_cms_foirequestlistcmsplugin', serialize=False, to='cms.CMSPlugin')),
                ('resolution', models.CharField(blank=True, choices=[('successful', 'Request Successful'), ('partially_successful', 'Request partially successful'), ('not_held', 'Information not held'), ('refused', 'Request refused'), ('user_withdrew_costs', 'Request was withdrawn due to costs'), ('user_withdrew', 'Request was withdrawn')], max_length=50)),
                ('status', models.CharField(blank=True, choices=[('awaiting_user_confirmation', 'Awaiting user confirmation'), ('publicbody_needed', 'Public Body needed'), ('awaiting_publicbody_confirmation', 'Awaiting Public Body confirmation'), ('awaiting_response', 'Awaiting response'), ('awaiting_classification', 'Request awaits classification'), ('asleep', 'Request asleep'), ('resolved', 'Request resolved')], max_length=50)),
                ('number_of_entries', models.PositiveIntegerField(default=1, help_text='0 means all the entries', verbose_name='number of entries')),
                ('offset', models.PositiveIntegerField(default=0, help_text='number of entries to skip from top of list', verbose_name='offset')),
                ('template', models.CharField(blank=True, choices=[('', 'Default template')], help_text='template used to display the plugin', max_length=250, verbose_name='template')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publicbody.Category')),
                ('classification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publicbody.Classification')),
                ('jurisdiction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publicbody.Jurisdiction')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foirequest.FoiProject')),
                ('publicbody', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publicbody.PublicBody')),
                ('tags', models.ManyToManyField(blank=True, to='taggit.Tag', verbose_name='tags')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]