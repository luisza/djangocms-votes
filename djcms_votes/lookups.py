# encoding: utf-8

'''
Free as freedom will be 24/9/2016

@author: luisza
'''

from __future__ import unicode_literals


from ajax_select import register, LookupChannel
from aldryn_newsblog.models import Article
from django.db.models.query_utils import Q
from aldryn_people.models import Person, Group
from aldryn_categories.models import Category


@register('articles')
class ArticleLookup(LookupChannel):

    model = Article

    def get_query(self, q, request):
        return self.model.objects.filter(
            Q(translations__title__icontains=q
              ) | Q(translations__lead_in__icontains=q)
        ).order_by('translations__slug')[:20]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.title


@register('categories')
class CategoryLookup(LookupChannel):

    model = Category

    def get_query(self, q, request):
        return self.model.objects.filter(
            translations__name__icontains=q).order_by('translations__name')[:20]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name


@register('people')
class PeopleLookup(LookupChannel):

    model = Person

    def get_query(self, q, request):
        return self.model.objects.filter(
            Q(translations__name__icontains=q
              ) | Q(user__first_name__icontains=q
                    ) | Q(user__last_name__icontains=q)
        ).order_by('translations__name')[:20]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name


@register('groups')
class GroupLookup(LookupChannel):

    model = Group

    def get_query(self, q, request):
        return self.model.objects.filter(
            Q(translations__name__icontains=q
              ) | Q(translations__description__icontains=q)).order_by(
                  'translations__name')[:20]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name
