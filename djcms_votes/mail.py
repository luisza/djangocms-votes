# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_comment(extra_context):

    send_mail("[site comment] %s" % (extra_context['subject']),
              extra_context['message'],
              settings.DEFAULT_FROM_EMAIL,
              settings.COMMENT_EMAIL_NOTIFICATION,
              fail_silently=True,
              html_message=render_to_string('djcms_votes/mail/comment.html',
                                            extra_context))
