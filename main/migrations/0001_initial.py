# Generated by Django 3.2.4 on 2021-06-17 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('contact_no', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('T', 'Transgender')], max_length=1)),
                ('identity_no', models.CharField(max_length=50)),
                ('id_proof', models.ImageField(upload_to='')),
            ],
            options={
                'ordering': ['first_name', 'middle_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('price', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_id', models.AutoField(primary_key=True, serialize=False)),
                ('no_of_children', models.PositiveSmallIntegerField(default=0)),
                ('no_of_adults', models.PositiveSmallIntegerField(default=1)),
                ('no_of_rooms', models.PositiveSmallIntegerField(default=1)),
                ('reservation_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('expected_arrival_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('expected_departure_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
            ],
            options={
                'permissions': (('can_view_reservation', 'Can view reservation'), ('can_view_reservation_detail', 'Can view reservation detail')),
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('profile_picture', models.ImageField(default='images/staff.png', upload_to='staff_img/')),
                ('staff_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('contact_no', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['first_name', 'middle_name', 'last_name'],
                'permissions': (('can_view_customer', 'Can view customer'),),
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('room_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('price', models.PositiveSmallIntegerField()),
                ('Max_no_of_guest', models.PositiveSmallIntegerField(default=True)),
                ('No_of_Rooms', models.PositiveSmallIntegerField(default=True)),
                ('facility', models.ManyToManyField(to='main.Facility')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_no', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('availability', models.BooleanField(default=0)),
                ('reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.reservation')),
                ('room_type', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.roomtype')),
            ],
            options={
                'ordering': ['room_no'],
                'permissions': (('can_view_room', 'Can view room'),),
            },
        ),
        migrations.AddField(
            model_name='reservation',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.staff'),
        ),
    ]
