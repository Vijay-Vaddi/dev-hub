from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
    
    # adding class to each field
        for name, field in self.fields.items():
                print('name :',name, 'field :', field)
                field.widget.attrs.update({'class':'input'})
                field.help_text = None

class EditProfileForm(ModelForm):
    class Meta:
         model = Profile
         exclude = ['user']