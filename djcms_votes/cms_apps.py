# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from . import DEFAULT_APP_NAMESPACE


class Djcms_VotesApp(CMSApp):
    name = _('Votes')
    urls = ['djcms_votes.app_urls']
    app_name = DEFAULT_APP_NAMESPACE

apphook_pool.register(Djcms_VotesApp)
