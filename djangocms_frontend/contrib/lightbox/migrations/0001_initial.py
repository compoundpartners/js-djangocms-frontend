from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('djangocms_frontend', '0002_auto_20221212_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lightbox',
            fields=[
            ],
            options={
                'verbose_name': 'Lightbox',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('djangocms_frontend.frontenduiitem',),
        ),
    ]
