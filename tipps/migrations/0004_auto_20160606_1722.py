# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipps', '0003_auto_20160606_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='team',
            field=models.CharField(choices=[(b'bn', b'Bonn'), (b'dafr', b'Darmstadt/Frankfurt'), (b'es', b'Essen'), (b'pdb', b'Paderborn'), (b'mz', b'Mainz'), (b'wu', b'Wuppertal')], max_length=10),
        ),
    ]
