from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic

from lending import mixins, forms
from lending.models import Book, Student, Lending, BibliographicPlan, StudyTopic


class BookListView(auth_mixins.LoginRequiredMixin, mixins.AjaxableListMixin):
    model = Book


class BookCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    model = Book
    success_url = reverse_lazy('lending:book-list')
    form_class = forms.BookCreateForm


class BookUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):  # no usado
    model = Book
    form_class = forms.BookUpdateForm

    def get_success_url(self):
        return reverse_lazy('lending:book-detail', kwargs={'pk': self.object.pk})


class BookDetailView(auth_mixins.LoginRequiredMixin, generic.DetailView):  # No usado
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BookDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):  # no usado
    model = Book
    success_url = reverse_lazy('lending:book-list')


class StudentDetailView(auth_mixins.LoginRequiredMixin, mixins.AjaxableDetailMixin):
    model = Student

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.filter(lending__student=kwargs['object'])
        return context


class StudentListView(auth_mixins.LoginRequiredMixin, mixins.AjaxableListMixin):
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


class StudentCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    model = Student
    form_class = forms.StudentCreateForm
    success_url = reverse_lazy('lending:student-query')


class StudentDeleteView(auth_mixins.LoginRequiredMixin, mixins.AjaxableDeleteMixin):
    model = Student
    success_url = reverse_lazy('lending:student-query')


class StudentUpdateView(auth_mixins.LoginRequiredMixin, mixins.AjaxableUpdateMixin):
    model = Student
    fields = ['first_name', 'last_name', 'ci', 'number', 'academic_year']

    def get_success_url(self):
        return reverse_lazy('lending:student-detail', kwargs={'pk': self.object.pk})


class LendingCreateView(auth_mixins.LoginRequiredMixin, mixins.AjaxableCreateMixin):
    model = Lending
    success_url = reverse_lazy('lending:student-query')
    fields = ['student', 'book']


class LendingQueryView(auth_mixins.LoginRequiredMixin, mixins.AjaxableListMixin):
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


class LendingDetailView(auth_mixins.LoginRequiredMixin, mixins.AjaxableDetailMixin):  # no usado
    model = Lending


class LendingDeleteView(auth_mixins.LoginRequiredMixin, mixins.AjaxableDeleteMixin):
    model = Lending
    success_url = reverse_lazy('lending:student-query')


class BibliographicPlanCreateView(auth_mixins.LoginRequiredMixin, mixins.AjaxableCreateMixin):
    model = BibliographicPlan
    form_class = forms.BibliographicPlanForm
    success_url = reverse_lazy('lending:bibliographic-list')


class BibliographicPlanDetailView(auth_mixins.LoginRequiredMixin, mixins.AjaxableDetailMixin):
    model = BibliographicPlan


class BibliographicPlanListView(auth_mixins.LoginRequiredMixin, mixins.AjaxableListMixin):
    model = BibliographicPlan


class BibliographicPlanUpdateView(auth_mixins.LoginRequiredMixin, mixins.AjaxableUpdateMixin):
    model = BibliographicPlan
    form_class = forms.BibliographicPlanForm
    success_url = reverse_lazy('lending:bibliographic-detail')


class BibliographicPlanDeleteView(auth_mixins.LoginRequiredMixin, mixins.AjaxableDeleteMixin):
    model = BibliographicPlan
    success_url = reverse_lazy('lending:bibliographic-list')


class StudyTopicCreateView(auth_mixins.LoginRequiredMixin, mixins.AjaxableCreateMixin):
    model = StudyTopic
    form_class = forms.StudyTopicForm
    success_url = reverse_lazy('lending:study-topic-list')


class StudyTopicDetailView(auth_mixins.LoginRequiredMixin, mixins.AjaxableDetailMixin):
    model = StudyTopic


class StudyTopicListView(auth_mixins.LoginRequiredMixin, mixins.AjaxableListMixin):
    model = StudyTopic


class StudyTopicUpdateView(auth_mixins.LoginRequiredMixin, mixins.AjaxableUpdateMixin):
    model = StudyTopic
    form_class = forms.StudyTopicForm
    success_url = reverse_lazy('lending:study-topic-list')


class StudyTopicDeleteView(auth_mixins.LoginRequiredMixin, mixins.AjaxableDeleteMixin):
    model = StudyTopic
    success_url = reverse_lazy('lending:study-topic-delete')
