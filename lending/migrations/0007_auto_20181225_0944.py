# Generated by Django 2.1.1 on 2018-12-25 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lending', '0006_auto_20181225_0932'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bibliographicplan',
            options={'verbose_name': 'Plan bibliográfico', 'verbose_name_plural': 'Planes bibliográficos'},
        ),
        migrations.AlterModelOptions(
            name='lending',
            options={'verbose_name': 'Préstamo', 'verbose_name_plural': 'Préstamos'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Estudiante', 'verbose_name_plural': 'Estudiantes'},
        ),
        migrations.AlterModelOptions(
            name='studytopic',
            options={'verbose_name': 'Asignatura', 'verbose_name_plural': 'Asignaturas'},
        ),
        migrations.AlterField(
            model_name='bibliographicplan',
            name='study_topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Asignatura', to='lending.StudyTopic'),
        ),
    ]