from django import forms

from lending import models


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Student
        exclude = ['books']

        widgets = {
            'academic_year': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }
