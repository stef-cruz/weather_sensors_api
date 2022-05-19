# Generated by Django 4.0.4 on 2022-05-15 14:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0005_sensor_sensor_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensordata',
            name='temperature_max',
        ),
        migrations.RemoveField(
            model_name='sensordata',
            name='temperature_min',
        ),
        migrations.AlterField(
            model_name='sensor',
            name='city_name',
            field=models.CharField(max_length=100, null=True, validators=[django.core.validators.RegexValidator('^[a-z_\\-]+$', 'Only lower case letters allowed.')]),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='country_name',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.RegexValidator('^[a-z_\\-]+$', 'Only lower case letters allowed.')]),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_nickname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
