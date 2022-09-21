import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class AddTaskForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['title'] = forms.CharField(required=True,
                                                label="",
                                                widget=forms.TextInput(attrs={'class': 'form-control dark-theme-element flex-fill',
                                                                              'placeholder': 'Title'}))
        self.fields['description'] = forms.CharField(required=False,
                                                     label="",
                                                     widget=forms.Textarea(attrs={'class': 'form-control dark-theme-element flex-fill',
                                                                                  'rows': '5',
                                                                                  'placeholder': 'Description'}))
        self.fields['target_date'] = forms.DateField(required=False,
                                                     initial=datetime.datetime.now,
                                                     widget=forms.DateInput(attrs={'type': 'date',
                                                                                   'class': 'form-control dark-theme-element text-secondary flex-fill me-2'}))
        self.fields['project'] = forms.ModelChoiceField(required=False,
                                                        queryset=Projects.objects.filter(user=kwargs['initial']['user']),
                                                        empty_label='Select project',
                                                        widget=forms.Select(attrs={'class': 'btn btn-outline-secondary dropdown-toggle'}))

    class Meta:
        model = Tasks
        fields = ['title', 'description', 'target_date', 'project']

    def clean_title(self):
        if len(self.cleaned_data['title']) > 50:
            raise ValidationError('Title can contain only 50 chars')
        return self.cleaned_data['title']


class DetailTaskForm(AddTaskForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['complete'] = forms.BooleanField(required=False,
                                                label="Done",
                                                widget=forms.CheckboxInput(attrs={'class': 'form-check-input dark-theme-element'}))

    class Meta:
        model = Tasks
        fields = ['complete', 'title', 'description', 'target_date', 'project']


class AddProjectForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['title'] = forms.CharField(required=True,
                                                label="",
                                                widget=forms.TextInput(attrs={'class': 'form-control dark-theme-element flex-fill',
                                                                              'placeholder': 'Title'}))
    class Meta:
        model = Projects
        fields = ['title']



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password1 = forms.CharField(label='Password', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '********'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '********'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
