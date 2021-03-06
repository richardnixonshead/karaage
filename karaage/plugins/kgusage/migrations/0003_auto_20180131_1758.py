# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-31 17:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kgusage', '0002_auto_20170831_1735'),
        ('karaage', '0004_auto_20160429_0927'),
    ]

    run_before = [
        ('karaage', '0005_auto_20171215_1831'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='institutecache',
            unique_together=set([('date', 'start', 'end', 'institute')]),
        ),
        migrations.RemoveField(
            model_name='institutecache',
            name='machine_category',
        ),
        migrations.AlterUniqueTogether(
            name='machinecategorycache',
            unique_together=set([('date', 'start', 'end')]),
        ),
        migrations.RemoveField(
            model_name='machinecategorycache',
            name='machine_category',
        ),
        migrations.AlterUniqueTogether(
            name='personcache',
            unique_together=set([('date', 'start', 'end', 'person', 'project')]),
        ),
        migrations.RemoveField(
            model_name='personcache',
            name='machine_category',
        ),
        migrations.AlterUniqueTogether(
            name='projectcache',
            unique_together=set([('date', 'start', 'end', 'project')]),
        ),
        migrations.RemoveField(
            model_name='projectcache',
            name='machine_category',
        ),
    ]
