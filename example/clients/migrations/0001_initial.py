# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 08:46
from __future__ import unicode_literals

import cloneable_model.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
            bases=(cloneable_model.models.CloneableModelMixin, models.Model),
        ),
    ]
