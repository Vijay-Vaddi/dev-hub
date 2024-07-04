from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = '__all__'
        exclude = ('vote_ratio','vote_total') #[]
    
    # to set a styling
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'style':'color:red'})

