# Generated by Django 5.0.1 on 2024-03-19 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('station_ID', models.AutoField(primary_key=True, serialize=False)),
                ('station_name', models.CharField(max_length=200)),
                ('station_address', models.CharField(max_length=200)),
                ('station_price', models.CharField(max_length=200)),
                ('station_phone', models.CharField(max_length=200)),
                ('station_email', models.EmailField(max_length=200)),
                ('station_caption', models.CharField(max_length=200)),
                ('station_latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('station_longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('station_image', models.ImageField(blank=True, null=True, upload_to='simages')),
                ('station_area', models.CharField(max_length=200)),
            ],
        ),
    ]