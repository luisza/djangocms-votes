# encoding: utf-8

'''
Free as freedom will be 12/9/2016

@author: luisza
'''

from __future__ import unicode_literals


from django.contrib.auth.forms import AuthenticationForm
from django import forms
from djcms_votes.models import Comment
from ajax_select.fields import AutoCompleteSelectMultipleField


class PollsForm(forms.Form):
    articles = AutoCompleteSelectMultipleField('articles', required=False)
    categories = AutoCompleteSelectMultipleField('categories', required=False)

    people = AutoCompleteSelectMultipleField('people', required=False)
    groups = AutoCompleteSelectMultipleField('groups', required=False)

    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)


class UserCommentForm(forms.ModelForm):
    page = forms.IntegerField(widget=forms.HiddenInput)
    appname = forms.CharField(widget=forms.HiddenInput)
    url = forms.URLField()

    class Meta:
        model = Comment
        fields = ["message", ]

# If you don't do this you cannot use Bootstrap CSS


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'name': 'password'}))
