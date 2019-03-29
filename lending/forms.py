from django import forms

from lending import models


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Student
        exclude = ['books']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.NumberInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.NumberInput(attrs={'min': 1, 'max': 6, 'class': 'form-control'})
        }


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'cant': forms.NumberInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publish_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'study_topic': forms.Select(attrs={'class': 'form-control'}),
        }


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['name', 'number', 'cant']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'cant': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StudyTopicForm(forms.ModelForm):
    class Meta:
        model = models.StudyTopic
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bibliographic_plan': forms.Select(attrs={'class': 'form-control'})
        }


class BibliographicPlanForm(forms.ModelForm):
    class Meta:
        model = models.BibliographicPlan
        fields = '__all__'

        widgets = {
            'year': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'career': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'modality': forms.Select(attrs={'class': 'form-control'}),
            'study_plan': forms.TextInput(attrs={'class': 'form-control'}),
        }
