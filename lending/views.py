from django.urls import reverse_lazy
from django.views import generic

from lending import mixins
from lending.models import Book, Student


class BookListView(generic.ListView):
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


class StudentDetailView(generic.DetailView):
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
