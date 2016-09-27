# encoding: utf-8

'''
Free as freedom will be 12/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from djcms_votes.models import get_app_name_models, Comment, Poll
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
import uuid


def randomword(length):
    return str(uuid.uuid4())[0:length]


def render_votes(page, as_view=False):
    appname, model = get_app_name_models(page).split(".")
    object_list = Comment.objects.filter(
        content_type=ContentType.objects.get(
            app_label=appname,
            model=model
        ),
        object_id=page.pk
    )
    stats = {
        'positive': object_list.filter(comment_type=Comment.POSITIVE).count(),
        'negative': object_list.filter(comment_type=Comment.NEGATIVE).count(),
        'neutral': object_list.filter(comment_type=Comment.NEUTRAL).count(),
    }

    appname, model = get_app_name_models(page).split(".")

    return render_to_string('djcms_votes/comment_chart.html',
                            {'page': page,
                             'object_list': object_list,
                             'appname': appname,
                             'model': model,
                             'stats': stats,
                             'as_view': as_view}
                            )


def render_polls(page, as_view=False):
    appname, model = get_app_name_models(page).split(".")
    object_list = Poll.objects.filter(
        content_type=ContentType.objects.get(
            app_label=appname,
            model=model
        ),
        object_id=page.pk
    )
    stats = {
        '1': object_list.filter(poll_type=1).count(),
        '2': object_list.filter(poll_type=2).count(),
        '3': object_list.filter(poll_type=3).count(),
        '4': object_list.filter(poll_type=4).count(),
        '5': object_list.filter(poll_type=5).count(),
    }

    appname, model = get_app_name_models(page).split(".")
    return render_to_string('djcms_votes/poll_chart.html',
                            {'page': page,
                             'object_list': object_list,
                             'appname': appname,
                             'model': model,
                             'stats': stats,
                             'as_view': as_view}
                            )


def render_poll_likes(appname, model, page_pk, user, poll=None):

    if poll is None:
        poll, created = Poll.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label=appname,
                model=model
            ),
            object_id=page_pk,
            user=user,
        )

    return render_to_string('djcms_votes/poll_likes.html',
                            {'object': poll,
                             'appname': appname,
                             'model': model,
                             'pk': page_pk,
                             'stars': [1, 2, 3, 4, 5]
                             }
                            )
