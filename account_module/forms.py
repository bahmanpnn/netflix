from django.forms import ModelForm, Form
from account_module.models import Profile


# from django import forms


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['uuid', 'avatar']
