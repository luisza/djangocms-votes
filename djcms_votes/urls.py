

from django.conf.urls import url
from djcms_votes import views
from django.contrib.auth.decorators import login_required
from djcms_votes.views import ListComment, comment_vote, get_stats

urlpatterns = [
    url(r'^create$', login_required(
        views.CreateComment.as_view()), name="comment_create"),

    url(r'list$', login_required(views.ListComment.as_view()),
        name="comment_list"),

    url(r'vote_comment/(?P<pk>\d+)/(?P<vote>\d+)$',
        views.comment_vote, name="comment_vote"),
    url(r'vote_poll/(?P<appname>\w+)/(?P<model>\w+)/(?P<pk>\d+)/(?P<vote>\d+)$',
        views.poll_vote, name="poll_vote"),
    url(r'vote_comment_char/(?P<appname>\w+)/(?P<model>\w+)/(?P<pk>\d+)$', views.show_comment_chart,
        name="vote_comment_chart"),
    url(r'poll_char/(?P<appname>\w+)/(?P<model>\w+)/(?P<pk>\d+)$', views.show_poll_chart,
        name="poll_chart"),
    url(r'user_votes/(?P<user>\d+)$',
        views.comments_per_user, name="user_votes"),

    url(r'vote_stats', get_stats, name="vote_stats")

]
