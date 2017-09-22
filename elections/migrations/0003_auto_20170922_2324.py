# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 23:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0002_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Votante',
                'verbose_name_plural': 'Votantes',
            },
        ),
        migrations.AlterModelOptions(
            name='election',
            options={'verbose_name': 'Elección', 'verbose_name_plural': 'Elecciones'},
        ),
        migrations.AlterModelOptions(
            name='list',
            options={'verbose_name': 'Lista', 'verbose_name_plural': 'Listas'},
        ),
        migrations.AddField(
            model_name='voter',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Election'),
        ),
    ]
