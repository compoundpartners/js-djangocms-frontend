# Generated by Django 3.2.16 on 2023-05-24 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_frontend', '0002_auto_20221212_1107'),
        ('custom_plugins', '0003_gatedcontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='GatedTrigger',
            fields=[
            ],
            options={
                'verbose_name': 'Gated Trigger',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('djangocms_frontend.frontenduiitem',),
        ),
    ]
