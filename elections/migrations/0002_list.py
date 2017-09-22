# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 23:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_description', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Election')),
            ],
        ),
    ]
