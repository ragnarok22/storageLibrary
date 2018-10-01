from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField(default=0)
    cant = models.PositiveIntegerField(default=0)

    def to_dict(self):
        return {
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
        through_fields=('student', 'book')
    )

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'ci': self.ci,
            'number': self.number,
            'academic_year': self.academic_year,
            # 'books': self.books,
        }


class Lending(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return '{} --> {}'.format(self.student, self.book)
