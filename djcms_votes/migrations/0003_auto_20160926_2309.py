# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djcms_votes', '0002_poll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='poll_type',
            field=models.SmallIntegerField(default=0, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]
