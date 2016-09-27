# encoding: utf-8

'''
Free as freedom will be 24/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from django.views.generic.list import ListView
from djcms_votes.models import Poll, Comment
from djcms_votes.forms import PollsForm
from django.views.generic.edit import ProcessFormView
from aldryn_people.models import Person
from aldryn_newsblog.models import Article
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import ugettext_lazy as _


class PollList(ListView, ProcessFormView):
    model = Poll
    template_name = 'djcms_votes/app/poll_list.html'
    form = PollsForm

    def get_contenttype_page(self):
        return ContentType.objects.get(app_label="aldryn_newsblog",
                                       model="article")

    def get_person_by_group(self, pks):
        people = [x[0] for x in Person.objects.filter(
            groups__pk__in=pks).values_list('pk')]

        return set(people)

    def get_articles(self, pks):
        articles = [x[0]
                    for x in Article.objects.filter(pk__in=pks).values_list('pk')]
        return set(articles)

    def get_articles_by_categories(self, pks):
        articles = [x[0]
                    for x in Article.objects.filter(
                        categories__pk__in=pks).values_list('pk')]
        return set(articles)

    def filter_query_with_form(self, form, query):
        if 'people' in form.cleaned_data and form.cleaned_data['people']:
            query = query.filter(
                user__persons__pk__in=form.cleaned_data['people'])

        if 'groups' in form.cleaned_data and form.cleaned_data['groups']:
            # FIXME: could be like, but sqlite not support distinct
            #
            query = query.filter(
                user__persons__pk__in=self.get_person_by_group(
                    form.cleaned_data['groups'])
            )
        if 'start_date' in form.cleaned_data and form.cleaned_data['start_date']:
            query = query.filter(
                created_date__gte=form.cleaned_data['start_date']
            )
        if 'end_date' in form.cleaned_data and form.cleaned_data['end_date']:
            query = query.filter(
                created_date__lte=form.cleaned_data['end_date']
            )

        if 'articles' in form.cleaned_data and form.cleaned_data['articles']:
            query = query.filter(
                content_type=self.get_contenttype_page(),
                object_id__in=self.get_articles(
                    form.cleaned_data['articles'])
            )
        if 'categories' in form.cleaned_data and form.cleaned_data['categories']:
            query = query.filter(
                content_type=self.get_contenttype_page(),
                object_id__in=self.get_articles_by_categories(
                    form.cleaned_data['categories'])
            )
        return query

    def get_queryset(self):
        form = self.get_form()
        query = ListView.get_queryset(self)
        if self.request.method == "POST":
            if form.is_valid():
                query = self.filter_query_with_form(form, query)
            else:
                query = query.none()
        return query

    def form_valid(self, form):
        return self.get(self.request)

    def form_invalid(self, form):
        return self.get(self.request)

    def get_form(self):
        if self.request.method == 'POST':
            form = self.form(self.request.POST)
            form.is_valid()
            return form
        return self.form()

    def get_form_context(self, context):
        context['form'] = self.get_form()
        return context

    def get_poll_stats(self, context):
        stats = {
            'data': [context['object_list'].filter(poll_type=6 - x).count()
                     for x in range(1, 6)],
            'label': ['\u2605' * (6 - x) for x in range(1, 6)]
        }
        stats['display'] = zip(stats['label'], stats['data'])
        context['total_polls'] = stats
        return context

    def get_comment_stats(self, context):
        query = Comment.objects.all()
        if self.request.method == "POST":
            form = self.get_form()
            if form.is_valid():
                query = self.filter_query_with_form(form, query)

        stats = {
            'data': [
                query.filter(comment_type=Comment.POSITIVE).count(),
                query.filter(comment_type=Comment.NEGATIVE).count(),
                query.filter(comment_type=Comment.NEUTRAL).count(),
            ],
            'label': [_('Positive'), _('Negative'), _('Neutral')]
        }
        stats['display'] = zip(stats['label'], stats['data'])
        context['total_comment'] = stats

        return context

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context = self.get_poll_stats(context)
        context = self.get_form_context(context)
        context = self.get_comment_stats(context)
        return context
