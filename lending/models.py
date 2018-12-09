from django.db import models
from django.urls import reverse_lazy


class CustomModel(models.Model):
    def to_dict(self):
        raise NotImplemented


class Book(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField(default=0)
    cant = models.PositiveIntegerField(default=0)

    def to_dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'number': self.number,
            'cant': self.cant
        }

    def __str__(self):
        return '{}, cant: {}'.format(self.name, self.cant)

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'


class Student(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=150)
    ci = models.CharField(max_length=11)
    number = models.PositiveIntegerField(default=0)
    academic_year = models.PositiveIntegerField(default=1)
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
        }
        if show_lending:
            queryset = Lending.objects.filter(student_id=self.id)
            lending = []
            for q in queryset:
                lending.append(q.to_dict(False))
            data['lending'] = lending
        return data


class Lending(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return '{} --> {}'.format(self.student, self.book)

    def to_dict(self, show_student=True):
        data = {
            'pk': self.pk,
            'book': self.book.to_dict(),
            'date': self.date,
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
