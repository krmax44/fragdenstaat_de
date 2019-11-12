# Generated by Django 2.2.4 on 2019-10-21 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('froide_payment', '0009_auto_20191017_1446'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fds_donation', '0003_donationformcmsplugin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationformcmsplugin',
            name='initial_interval',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salutation', models.CharField(blank=True, max_length=25)),
                ('first_name', models.CharField(blank=True, max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=256)),
                ('company_name', models.CharField(blank=True, max_length=256)),
                ('address', models.CharField(blank=True, max_length=256)),
                ('city', models.CharField(blank=True, max_length=256)),
                ('postcode', models.CharField(blank=True, max_length=20)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('first_donation', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_donation', models.DateTimeField(default=django.utils.timezone.now)),
                ('email_confirmation_sent', models.DateTimeField(blank=True, null=True)),
                ('email_confirmed', models.DateTimeField(blank=True, null=True)),
                ('contact_allowed', models.BooleanField(default=False)),
                ('become_user', models.BooleanField(default=False)),
                ('receipt', models.BooleanField(default=False)),
                ('note', models.TextField()),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='froide_payment.Subscription')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'donor',
                'verbose_name_plural': 'donors',
                'ordering': ('-first_donation',),
            },
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('received', models.BooleanField(default=False)),
                ('note', models.TextField()),
                ('reference', models.CharField(blank=True, max_length=255)),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fds_donation.Donor')),
                ('order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='froide_payment.Order')),
                ('payment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='froide_payment.Payment')),
            ],
            options={
                'verbose_name': 'donation',
                'verbose_name_plural': 'donations',
                'ordering': ('-timestamp',),
            },
        ),
    ]
