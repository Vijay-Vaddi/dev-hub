from django.forms import ModelForm, widgets
from django import forms
from .models import Project, Review



class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = '__all__'
        # exclude = ('vote_ratio','vote_total') #[]
        fields = [ 'title', 'description', 'demo_link',
                   'source_code', 'project_image'
        ]

        # another way of styling, define within the meta class
        widgets = {
                'tags': forms.CheckboxSelectMultiple(),
            }   
        
    # to set a styling ['model_item_identifier']
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        # self.fields['title'].widget.attrs.update({'class':'input input--text', 
        #                                           'placeholder':'Project Title'})
       
        # adding class to each field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text'})

        # check if exclude can be used


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']

        labels = {
            'value': 'Place your vote',
            'body': 'Write your review here...'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})