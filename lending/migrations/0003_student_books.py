# Generated by Django 2.1.1 on 2018-10-01 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lending', '0002_auto_20180930_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='books',
            field=models.ManyToManyField(through='lending.Lending', to='lending.Book'),
        ),
    ]
