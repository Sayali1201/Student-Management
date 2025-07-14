from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'  # include all fields
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'}),
        }
