# encoding: utf-8

'''
Free as freedom will be 11/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from django_ajax.mixin import AJAXMixin
from django.views.generic.edit import CreateView
from djcms_votes.models import Comment, Poll
# Create your views here.

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from djcms_votes.forms import UserCommentForm
from django_ajax.decorators import ajax
from django.template.loader import render_to_string
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from djcms_votes.utils import render_votes, render_polls, render_poll_likes
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from djcms_votes.mail import send_comment


class CreateComment(AJAXMixin, CreateView):
    model = Comment
    form_class = UserCommentForm
    success_url = "/"

    def form_valid(self, form):
        app_label, model = form.cleaned_data['appname'].split(".")
        page_type = ContentType.objects.get(app_label=app_label,
                                            model=model)
        page = page_type.get_object_for_this_type(pk=form.cleaned_data['page'])
        if not page:
            raise
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.content_object = page
        self.object.save()
        context = {
            'subject': _("New comment available"),
            'message': self.object.message,
            'page': page,
            'comment': self.object,
            'request': self.request,
            'url': form.cleaned_data['url']

        }
        send_comment(context)
        return {
            'fragments': {
                '#comment_field': _("Thanks, your comment was received")
            },
        }

    def form_invalid(self, form):
        response = CreateView.form_invalid(self, form)
        response.render()
        return {
            'fragments': {
                '#comment_field': response.content
            },
        }


class ListComment(AJAXMixin, ListView):
    model = Comment
    paginate_by = 10

    def extract_get_params(self):
        self.page_appname = self.request.GET.get("appname", None)
        self.page_model = self.request.GET.get("model", None)
        self.page_pk = self.request.GET.get("pk", None)
        return all((self.page_appname, self.page_model, self.page_pk))

    def get_queryset(self):
        queryset = ListView.get_queryset(self)

        if not self.request.user.is_superuser:
            return queryset.none()

        if not self.extract_get_params():
            return queryset.none()

        queryset = queryset.filter(
            content_type=ContentType.objects.get(
                app_label=self.page_appname,
                model=self.page_model
            ),
            object_id=self.page_pk
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['appname'] = self.page_appname
        context['model'] = self.page_model
        context['pk'] = self.page_pk
        return context

    def get(self, request, *args, **kwargs):
        response = ListView.get(self, request, *args, **kwargs)
        response.render()
        return {
            'fragments': {
                '#comment_list': response.content
            },
        }


@ajax
@login_required
def comment_vote(request, pk, vote):
    dev = ""
    try:
        if request.user.is_superuser:
            if vote in ['1', '2', '3']:
                comment = Comment.objects.get(pk=pk)
                comment.comment_type = int(vote)
                comment.save()
                dev = render_to_string(
                    'djcms_votes/likes.html',
                    {'object': comment,
                     'pk': pk}
                )
    except:
        pass
    return {
        'fragments': {
            '#comment_vote_%(pk)s' % {'pk': pk}: dev
        },
    }


@ajax
@login_required
def show_comment_chart(request, appname, model, pk):
    pagect = ContentType.objects.get(app_label=appname, model=model)
    page = pagect.get_object_for_this_type(pk=pk)
    dev = ""
    if request.user.is_superuser:
        dev = render_votes(page, as_view=True)
    return {
        'fragments': {
            '#comment_chart': dev
        },
    }


@ajax
@login_required
def poll_vote(request, appname, model, pk, vote):
    dev = ""
    try:
        if vote in ['1', '2', '3', '4', '5']:
            poll = Poll.objects.get(
                content_type=ContentType.objects.get(
                    app_label=appname,
                    model=model
                ),
                object_id=pk,
                user=request.user
            )
            poll.poll_type = int(vote)
            poll.save()
            dev = render_poll_likes(
                appname, model, pk, request.user, poll=poll)
    except:
        pass
    return {
        'fragments': {
            '#poll_vote': dev
        },
    }


@ajax
def show_poll_chart(request, appname, model, pk):
    pagect = ContentType.objects.get(app_label=appname, model=model)
    page = pagect.get_object_for_this_type(pk=pk)
    dev = render_polls(page, as_view=True)
    return {
        'fragments': {
            '#poll_chart': dev
        },
    }


@ajax
@login_required
def comments_per_user(request, user):
    # FIXME: usuario solo con permisos puede ver esto
    User = get_user_model()
    user = get_object_or_404(User, pk=user)
    object_list = Comment.objects.filter(
        user=user
    )

    stats = {
        'positive': object_list.filter(comment_type=Comment.POSITIVE).count(),
        'negative': object_list.filter(comment_type=Comment.NEGATIVE).count(),
        'neutral': object_list.filter(comment_type=Comment.NEUTRAL).count(),
    }
    return render(request, 'djcms_votes/user_votes.html', {
        'user': user,
        'stats': stats
    })


@login_required
def get_stats(request):
    pass
