# Generated by Django 3.0.5 on 2020-05-28 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('froide_payment', '0013_auto_20200528_1201'),
        ('fds_donation', '0020_auto_20200523_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='froide_payment.Subscription'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='recurring_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='donor',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='froide_payment.Subscription'),
        ),
    ]
