from .models import Task 
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task ## importa modelo task para crear formulario
        fields = ['title','description','important']
        widgets = {##estilizar paginar de crear tarea desder forms django
            'title' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Write a title'}),
            'description' : forms.Textarea(attrs={'class':'form-control','placeholder':'Write a description'}),
            'important' : forms.CheckboxInput(attrs={'class':'form-check-input'})
        }