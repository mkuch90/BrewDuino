# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrewSettings',
            fields=[
                ('date_time', models.FloatField(serialize=False, primary_key=True)),
                ('system_on', models.IntegerField()),
                ('coil_unlocked', models.IntegerField()),
                ('control_mode', models.IntegerField()),
                ('boil_temp', models.IntegerField()),
                ('mash_temp', models.IntegerField()),
                ('coil_power', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('date_time', models.FloatField(serialize=False, primary_key=True)),
                ('coil_on', models.IntegerField()),
                ('coil_power', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('date_time', models.FloatField(serialize=False, primary_key=True)),
                ('boil_temp', models.IntegerField()),
                ('mash_temp', models.IntegerField()),
                ('stream_temp', models.IntegerField()),
            ],
        ),
    ]
