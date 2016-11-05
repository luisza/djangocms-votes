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
from django.utils.translation import ugettext_lazy as _


class PollsForm(forms.Form):
    articles = AutoCompleteSelectMultipleField('articles', required=False, 
        label=_('Articles'))
    categories = AutoCompleteSelectMultipleField('categories', required=False,
        label=_('Categories'))

    people = AutoCompleteSelectMultipleField('people', required=False,
        label=_('People'))
    groups = AutoCompleteSelectMultipleField('groups', required=False,
        label=_('Groups'))

    start_date = forms.DateField(required=False, label=_('Start date'))
    end_date = forms.DateField(required=False, label=_('End date'))


class UserCommentForm(forms.ModelForm):
    page = forms.IntegerField(widget=forms.HiddenInput)
    appname = forms.CharField(widget=forms.HiddenInput)
    url = forms.URLField()

    class Meta:
        model = Comment
        fields = ["message", ]

# If you don't do this you cannot use Bootstrap CSS


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label=_("Password"), max_length=30,
                                
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'name': 'password'}))
