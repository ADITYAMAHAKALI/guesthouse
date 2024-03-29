# Generated by Django 3.2.4 on 2021-06-19 03:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.CharField(blank=True, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('rooms', models.CharField(blank=True, editable=False, max_length=50)),
                ('initial_amount', models.PositiveSmallIntegerField(blank=True, editable=False)),
                ('check_in_date_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('last_edited_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('reservation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.reservation')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stay_duration', models.DurationField(editable=False, null=True)),
                ('total_amount', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('pay_amount', models.PositiveSmallIntegerField(default=0, editable=False)),
                ('check_out_date_time', models.DateTimeField(editable=False, null=True)),
                ('check_in', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='payments.checkin')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
