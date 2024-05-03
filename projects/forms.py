from django.forms import ModelForm
from .models import Project

class Create_project_form(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'