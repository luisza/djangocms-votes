# encoding: utf-8


'''
Created on 31/10/2016

@author: luisza
'''
from __future__ import unicode_literals


bucket_list = []


def register_bucket(bucket):
    bucket_list.append(bucket)


def get_bucketlist():
    return bucket_list


class Basebucket(object):
    title = ""
    abstract = False
    name = "basebucket"
    model_class=None

    def get_title(self):
        return self.title

    def get_labels(self):
        return []

    def get_graph(self, queryset, form):
        return "HTML here"

    def get_data_display(self, queryset, form):
        return "HTML"

    def allow_queryset(self, queryset):
        return False

    def get_queryset(self):
        return self.model_class.objects.all()

    def filter_query(self, queryset, form):
        return queryset

    def get_form(self, request):
        # form
        return None
