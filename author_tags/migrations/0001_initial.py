# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0002_auto_20150806_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authortags',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('age_range_tags', models.CharField(default=0, max_length=10, null=True, blank=True, choices=[(b'All', b'All'), (b'10-14', b'10-14'), (b'15-19', b'15-19'), (b'20-24', b'20-24'), (b'25+', b'25+')])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
