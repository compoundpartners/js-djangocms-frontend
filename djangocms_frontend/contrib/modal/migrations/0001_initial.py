# Generated by Django 3.2.16 on 2023-03-13 10:04

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('djangocms_frontend', '0002_auto_20221212_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modal',
            fields=[
            ],
            options={
                'verbose_name': 'Modal',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('djangocms_frontend.frontenduiitem',),
        ),
    ]
