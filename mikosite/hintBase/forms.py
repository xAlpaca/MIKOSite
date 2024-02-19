from django import forms
from .models import Problem
from formtools.preview import FormPreview

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ["latex_code","author", "source", "image", "difficulty", "tags"]
        
