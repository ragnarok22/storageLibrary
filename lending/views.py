from django.urls import reverse_lazy
from django.views import generic

from lending import mixins, forms
from lending.models import Book, Student, Lending


class BookListView(mixins.AjaxableListMixin):
    model = Book


class BookCreateView(generic.CreateView):
    model = Book
    success_url = reverse_lazy('lending:book-list')
    fields = ['name', 'number', 'cant']


class BookUpdateView(generic.UpdateView):
    model = Book
    fields = ['name', 'number', 'cant']

    def get_success_url(self):
        return reverse_lazy('lending:book-detail', kwargs={'pk': self.object.pk})


class BookDetailView(generic.DetailView):  # No usado
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookDeleteView(generic.DeleteView):
    model = Book
    success_url = reverse_lazy('lending:book-list')


class StudentDetailView(mixins.AjaxableDetailMixin):
    model = Student

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.filter(lending__student=kwargs['object'])
        return context


class StudentListView(mixins.AjaxableListMixin):
    model = Student

    def get_queryset(self):
        type_query = self.request.GET.get('type')
        query = self.request.GET.get('q')
        if type_query == 'name':
            students = Student.objects.filter(first_name__contains=query)
        elif type_query == 'last_name':
            students = Student.objects.filter(last_name__contains=query)
        elif type_query == 'number':
            students = Student.objects.filter(number=query)
        else:
            students = Student.objects.all()
        return students

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', None)
        context['type'] = self.request.GET.get('type', None)
        return context


class StudentCreateView(generic.CreateView):
    model = Student
    form_class = forms.StudentCreateForm
    success_url = reverse_lazy('lending:student-query')


class StudentDeleteView(mixins.AjaxableDeleteMixin):
    model = Student
    success_url = reverse_lazy('lending:student-query')


class StudentUpdateView(generic.UpdateView, mixins.AjaxablePostMixin):
    model = Student
    fields = ['first_name', 'last_name', 'ci', 'number', 'academic_year']

    def get_success_url(self):
        return reverse_lazy('lending:student-detail', kwargs={'pk': self.object.pk})


class LendingCreateView(mixins.AjaxablePostMixin, generic.CreateView):
    model = Lending
    success_url = reverse_lazy('lending:student-query')
    fields = ['student', 'book']


class LendingQueryView(mixins.AjaxableListMixin):
    model = Lending

    def get_queryset(self):
        student_pk = self.request.GET.get('student', None)
        book_pk = self.request.GET.get('book', None)

        if student_pk:
            return Lending.objects.filter(student_pk=student_pk)
        elif book_pk:
            return Lending.objects.filter(book_pk=book_pk)
        else:
            return super().get_queryset()


class LendingDetailView(mixins.AjaxableDetailMixin):
    model = Lending


class LendingDeleteView(mixins.AjaxableDeleteMixin):
    model = Lending
    success_url = reverse_lazy('lending:student-query')
