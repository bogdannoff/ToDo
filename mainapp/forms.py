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
                                                widget=forms.TextInput(attrs={'class': 'text-input',
                                                                              'placeholder': 'Title'}))
        self.fields['description'] = forms.CharField(required=False,
                                                     label="",
                                                     widget=forms.Textarea(attrs={'class': 'text-input',
                                                                                  'rows': '5',
                                                                                  'placeholder': 'Description'}))
        self.fields['target_date'] = forms.DateField(required=False,
                                                     initial=datetime.datetime.now,
                                                     widget=forms.DateInput(attrs={'type': 'date',
                                                                                   'class': 'form-control me-2'}))
        self.fields['project'] = forms.ModelChoiceField(required=False,
                                                        queryset=Projects.objects.all(),
                                                        empty_label='Select project',
                                                        widget=forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}))

    class Meta:
        model = Tasks
        fields = ['title', 'description', 'target_date', 'project']
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'text-input'}),
        #     'description': forms.Textarea(attrs={'class': 'text-input'}),
        #     'target_date': forms.DateInput(attrs={'type': 'date',
        #                                           'class': 'form-control me-2'},
        #                                    format='%Y-%m-%dT%H:%M'),
        #     'project': forms.Select(attrs={'class': 'dropdown'}),
        # }


    def clean_title(self):
        if len(self.cleaned_data['title']) > 50:
            raise ValidationError('Title can contain only 50 chars')
        return self.cleaned_data['title']


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
