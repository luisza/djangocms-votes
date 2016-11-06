# encoding: utf-8

'''
Free as freedom will be 24/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from aldryn_newsblog.models import Article
from aldryn_people.models import Person
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from django.views.generic.edit import ProcessFormView
from django.views.generic.list import ListView
from djcms_votes.bucket import views

BucketView = views.BucketView
