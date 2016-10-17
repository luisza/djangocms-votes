# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_client import forms


class Form(forms.BaseForm):
    comment_notification_email = forms.CharField(
        'List of notification email (comma separated)',
        required=True
    )

    def to_settings(self, data, settings):
        emails = data.get('comment_notification_email', '')
        settings['COMMENT_EMAIL_NOTIFICATION'] = emails.split(",")

        try:
            settings['ADDON_URLS'].append('djcms_votes.requirements_urls')

        except:
            settings['ADDON_URLS'] = ['djcms_votes.requirements_urls']


        return settings
