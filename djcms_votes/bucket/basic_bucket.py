# encoding: utf-8


'''
Created on 31/10/2016

@author: luisza
'''
from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from djcms_votes.bucket import Basebucket, register_bucket
from djcms_votes.forms import PollsForm
from djcms_votes.models import Poll, Comment


class PeopleArticule(Basebucket):
    abstract = True
    name = "default"
    model_class = Poll

    def __init__(self, name="default", abstract=True):
        self.abstract = abstract
        self.name = name

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

    def get_form(self, request):
        if request.method == 'POST':
            return (self.name, PollsForm(request.POST))
        if self.abstract:
            return (self.name, PollsForm())
        return (self.name, None)

    def filter_query(self, query, form):

        if form is None:
            return query
        form.is_valid()
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


class Comments(Basebucket):
    title = _("Comments")
    pa = None
    name = "comment"
    model_class = Comment

    def allow_queryset(self, queryset):
        if queryset.model.__name__ == self.model_class.__name__:
            return True
        return False

    def __init__(self):
        self.pa = PeopleArticule(name=self.name, abstract=False)

    def get_form(self, request):
        return self.pa.get_form(request)

    def filter_query(self, query, form):
        return self.pa.filter_query(query, form)

    def get_data_display(self, queryset, form):
        queryset = queryset[0]
        stats = {
            'data': [
                queryset.filter(comment_type=Comment.POSITIVE).count(),
                queryset.filter(comment_type=Comment.NEGATIVE).count(),
                queryset.filter(comment_type=Comment.NEUTRAL).count(),
            ],
            'label': [_('Positive'), _('Negative'), _('Neutral')]
        }
        stats['display'] = zip(stats['label'], stats['data'])

        return stats

    def get_graph(self, queryset, form):
        stats = self.get_data_display(queryset, form)

        labels = """[%s]""" % (
            ", ".join(['"' + str(x) + '"' for x in stats['label']]),)

        dataset = {
            'data' : """[%s]""" % (", ".join([str(x) for x in stats['data']])),


            'backgroundColor' : """[
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)'
            ]""",

            'borderColor' : """[
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ]""",
            'label': _('Total comments')
        }
        return render_to_string('djcms_votes/app/graph.html',
                                {
                                    'graph_type': 'bar',
                                    'labels': labels,
                                    'datasets': [
                                        dataset
                                    ],
                                    'name': "graphic_" + self.name
                                }
                                )


class Poll(Basebucket):
    title = _("Polls")
    pa = None
    name = "poll"
    model_class = Poll

    def __init__(self):
        self.pa = PeopleArticule(name=self.name, abstract=False)

    def allow_queryset(self, queryset):
        if queryset.model.__name__ == self.model_class.__name__:
            return True
        return False

    def filter_query(self, query, form):
        return self.pa.filter_query(query, form)

    def get_form(self, request):
        return self.pa.get_form(request)

    def get_data_display(self, queryset, form):
        queryset = queryset[0]
        stats = {
            'data': [queryset.filter(poll_type=6 - x).count()
                     for x in range(1, 6)],
            'label': ['\u2605' * (6 - x) for x in range(1, 6)]
        }
        stats['display'] = zip(stats['label'], stats['data'])

        return stats

    def get_graph(self, queryset, form):
        stats = self.get_data_display(queryset, form)
        labels = """[%s]""" % (
            ", ".join(['"' + str(x) + '"' for x in stats['label']]),)

        dataset = {
            'data' : """[%s]""" % (", ".join([str(x) for x in stats['data']])),


            'backgroundColor' : """[
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)'
            ]""",

            'borderColor' : """[
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ]""",
            'label': _('Total starts')
        }
        return render_to_string('djcms_votes/app/graph.html',
                                {
                                    'graph_type': 'bar',
                                    'labels': labels,
                                    'datasets': [
                                        dataset
                                    ],
                                    'name': "graphic_" + self.name
                                }
                                )


register_bucket(PeopleArticule())
register_bucket(Poll())
register_bucket(Comments())
