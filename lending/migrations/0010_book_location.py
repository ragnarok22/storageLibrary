# Generated by Django 2.1.1 on 2019-03-29 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lending', '0009_auto_20190313_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='location',
            field=models.CharField(default='Holguin', max_length=100, verbose_name='Localidad'),
            preserve_default=False,
        ),
    ]
