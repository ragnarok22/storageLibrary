from django import forms

from lending import models


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Student
        exclude = ['books']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.NumberInput(attrs={'min': 1, 'max': 6, 'class': 'form-control'})
        }
