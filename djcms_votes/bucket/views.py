# encoding: utf-8


'''
Created on 31/10/2016

@author: luisza
'''
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.base import View

from djcms_votes.bucket import get_bucketlist
from djcms_votes.bucket.basic_bucket import *
from djcms_votes.models import Poll


class BucketView(View):
    template_name = "djcms_votes/app/bucket.html"
    model_class = Poll

    def get(self, request, *args, **kwargs):
        forms = {}
        graphics = []
        querys = {}
        for bucketobj in get_bucketlist():
            query = bucketobj.get_queryset()
            if query.model.__name__ not in querys:
                querys[query.model.__name__] = query

        for bucketobj in get_bucketlist():
            name, form = bucketobj.get_form(request)
            if not bucketobj.abstract:
                query = [
                    q for n, q in querys.items() if bucketobj.allow_queryset(q)]
                graphics.append({
                    'data': bucketobj.get_data_display(query, form),
                    'plot': bucketobj.get_graph(query, form),
                    'title': bucketobj.get_title(),
                    'bucket': bucketobj,
                    'name': bucketobj.name,
                })

            if form:
                forms[name] = form

        return render(request, self.template_name,
                      {
                          'forms': forms,
                          'graphics': graphics,
                          'query': query
                      }
                      )

    def post(self, request, *args, **kwargs):
        forms = {}
        graphics = []

        querys = {}
        for bucketobj in get_bucketlist():
            query = bucketobj.get_queryset()
            if query.model.__name__ not in querys:
                querys[query.model.__name__] = query

        for bucketobj in get_bucketlist():
            name, form = bucketobj.get_form(request)
            if not bucketobj.abstract:
                for qname, query in querys.items():
                    if bucketobj.allow_queryset(query):
                        query = bucketobj.filter_query(query, form)
                        querys[query.model.__name__] = query
            if form:
                forms[name] = form

        for bucketobj in get_bucketlist():
            if not bucketobj.abstract:
                allow_querys = [
                    q for n, q in querys.items() if bucketobj.allow_queryset(q)]
                graphics.append({
                    'data': bucketobj.get_data_display(allow_querys, form),
                    'plot': bucketobj.get_graph(allow_querys, form),
                    'title': bucketobj.get_title(),
                    'bucket': bucketobj,
                    'name': bucketobj.name,
                })

        return render(request, self.template_name,
                      {
                          'forms': forms,
                          'graphics': graphics,
                          'query': querys
                      }
                      )
