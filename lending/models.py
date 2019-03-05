from django.db import models
from django.urls import reverse_lazy


class Book(models.Model):
    name = models.CharField('Nombre', max_length=100)
    number = models.PositiveIntegerField('Número', default=0)
    cant = models.PositiveIntegerField('Cantidad', default=0)
    author = models.CharField('Autor', max_length=200)
    publish_year = models.PositiveSmallIntegerField('Año de publicación')
    editorial = models.CharField('Editorial', max_length=100)
    study_topic = models.ForeignKey('StudyTopic', models.CASCADE, verbose_name='Asignatura')

    def to_dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'number': self.number,
            'cant': self.cant,
            'author': self.author,
            'publish_year': self.publish_year,
            'editorial': self.editorial,
            'study_topic': self.study_topic.to_dict()
        }

    def __str__(self):
        return '{}, cant: {}'.format(self.name, self.cant)

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'


class Student(models.Model):
    first_name = models.CharField('Nombre', max_length=80)
    last_name = models.CharField('Apellidos', max_length=150)
    ci = models.CharField('CI', max_length=11)
    number = models.PositiveIntegerField('Número', default=0)
    academic_year = models.PositiveIntegerField('Año académico', default=1)
    books = models.ManyToManyField(
        Book,
        through='Lending',
        through_fields=('student', 'book'),
        blank=True
    )

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_detail_url(self):
        return reverse_lazy('lending:student-detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse_lazy('lending:student-delete', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse_lazy('lending:student-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.get_full_name()

    def to_dict(self, show_lending=True):
        data = {
            'pk': self.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'ci': self.ci,
            'number': self.number,
            'academic_year': self.academic_year,
            'detail_url': self.get_detail_url(),
            'update_url': self.get_update_url(),
            'delete_url': self.get_delete_url(),
        }
        if show_lending:
            queryset = Lending.objects.filter(student_id=self.id)
            lending = []
            for q in queryset:
                lending.append(q.to_dict(False))
            data['lending'] = lending
        return data

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'


class Lending(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField('Fecha', auto_now=True)

    def __str__(self):
        return '{} --> {}'.format(self.student, self.book)

    def get_delete_url(self):
        return reverse_lazy('lending:lending-delete', kwargs={'pk': self.pk})

    def to_dict(self, show_student=True):
        data = {
            'pk': self.pk,
            'book': self.book.to_dict(),
            'date': self.date,
            'delete_url': self.get_delete_url(),
        }
        if show_student:
            data['student'] = self.student.to_dict(False)
        return data

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.book.cant -= 1
        self.book.save()
        return super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        self.book.cant += 1
        self.book.save()
        return super().delete(using, keep_parents)

    class Meta:
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'


class BibliographicPlan(models.Model):
    MODALITY_CHOICES = (
        ('CD', 'Curso Regular Diurno'),
        ('CE', 'Curso por encuentro'),
    )
    SEMESTER_CHOICES = (
        ('1', 'Primer Semestre'),
        ('2', 'Segundo Semestre'),
    )

    YEAR_CHOICES = (
        (1, 'Primero'),
        (2, 'Segundo'),
        (3, 'Tercero'),
        (4, 'Cuarto'),
        (5, 'Quinto'),
        (6, 'Sexto'),
    )

    year = models.PositiveSmallIntegerField('Año', choices=YEAR_CHOICES)
    semester = models.CharField('Semestre', max_length=1, choices=SEMESTER_CHOICES)
    career = models.CharField('Carrera', max_length=100)
    course = models.CharField('Curso', max_length=10)
    modality = models.CharField('Modalidad', max_length=2, choices=MODALITY_CHOICES)
    study_plan = models.CharField('Plan de estudio', max_length=3)

    def __str__(self):
        return 'Plan bibliográfico de la carrera {}. Curso {}'.format(self.career, self.course)

    class Meta:
        verbose_name = 'Plan bibliográfico'
        verbose_name_plural = 'Planes bibliográficos'

    def to_dict(self):
        return {
            'pk': self.pk,
            'year': self.year,
            'career': self.career,
            'modality': self.modality,
            'study_plan': self.study_plan,
            'course': self.course,
            'semester': self.semester
        }


class StudyTopic(models.Model):
    name = models.CharField('Asignatura', max_length=100)
    bibliographic_plan = models.ForeignKey('BibliographicPlan', models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'

    def to_dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'bibliographic_plan': self.bibliographic_plan.to_dict(),
        }
