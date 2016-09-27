# encoding: utf-8

'''
Free as freedom will be 11/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from classytags.core import Options
from classytags.helpers import Tag
from classytags.arguments import Argument
from django import template
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from djcms_votes.forms import UserCommentForm
from djcms_votes.models import get_app_name_models
from djcms_votes.utils import render_votes, render_polls, render_poll_likes
from djcms_votes.forms import LoginForm

register = template.Library()


class Render_Comments(Tag):
    name = 'render_comments'
    options = Options(
        Argument('page', required=True),
    )

    def render_tag(self, context, page):
        if 'request' not in context:
            return ""
        else:
            request = context['request']
            user = request.user
        if not user.is_active:
            return render_to_string(
                'djcms_votes/login.html',
                {'form': LoginForm(),
                 'next': request.path},
                request=request
            )

        if user.is_superuser:
            appname, model = get_app_name_models(page).split(".")
            return render_to_string('djcms_votes/comments_display.html',
                                    {'page': page,
                                     'appname': appname,
                                     'model': model,

                                     })

        return render_to_string('djcms_votes/comment_form.html',
                                {'page': page,
                                 'appname': get_app_name_models(page),
                                 'request': request,
                                 'form': UserCommentForm})

register.tag(Render_Comments)


class Render_Chart(Tag):
    name = 'render_comment_chart'
    options = Options(
        Argument('page', required=True),
    )

    def render_tag(self, context, page):
        if 'request' not in context:
            return ""
        else:
            request = context['request']
            user = request.user
        if not user.is_superuser:
            return ""

        return render_votes(page)

register.tag(Render_Chart)


class Render_Poll(Tag):
    name = 'render_poll'
    options = Options(
        Argument('page', required=True),
    )

    def render_tag(self, context, page):
        if 'request' not in context:
            return ""
        else:
            request = context['request']
            user = request.user
        # if not user.is_superuser:
        #    return ""

        return render_polls(page)

register.tag(Render_Poll)


class Render_Poll_Likes(Tag):
    name = 'render_poll_likes'
    options = Options(
        Argument('page', required=True),
    )

    def render_tag(self, context, page):
        if 'request' not in context:
            return ""
        else:
            request = context['request']
            user = request.user
        if user is None or user.is_anonymous():
            return _("Loggin to rate")
        # if not user.is_superuser:
        #    return ""
        appname, model = get_app_name_models(page).split(".")
        return render_poll_likes(appname, model, page.pk, user)

register.tag(Render_Poll_Likes)
