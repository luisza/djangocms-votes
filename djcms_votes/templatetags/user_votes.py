from classytags.core import Options
from classytags.helpers import Tag
from classytags.arguments import Argument
from django import template
from django.template.loader import render_to_string
from djcms_votes.models import get_app_name_models, Poll, Comment
from djcms_votes.utils import randomword

register = template.Library()


class User_Poll_Likes(Tag):
    name = 'user_poll_likes_chart'
    options = Options(
        Argument('user', required=True),
    )

    def render_tag(self, context, user):
        if 'request' not in context:
            return ""

        object_list = Poll.objects.filter(
            user=user,
        )

        stats = {
            '1': object_list.filter(poll_type=1).count(),
            '2': object_list.filter(poll_type=2).count(),
            '3': object_list.filter(poll_type=3).count(),
            '4': object_list.filter(poll_type=4).count(),
            '5': object_list.filter(poll_type=5).count(),
        }

        return render_to_string('djcms_votes/user_poll_chart.html',
                                {'user': user,
                                 'stats': stats,
                                 'id': randomword(5)
                                 }
                                )


register.tag(User_Poll_Likes)


class User_comment_Likes(Tag):
    name = 'user_comment_likes_chart'
    options = Options(
        Argument('user', required=True),
    )

    def render_tag(self, context, user):
        if 'request' not in context:
            return ""

        object_list = Comment.objects.filter(
            user=user,
        )

        stats = {
            'positive': object_list.filter(comment_type=Comment.POSITIVE).count(),
            'negative': object_list.filter(comment_type=Comment.NEGATIVE).count(),
            'netural': object_list.filter(comment_type=Comment.NEUTRAL).count(),
        }

        return render_to_string('djcms_votes/user_comment_chart.html',
                                {'user': user,
                                 'stats': stats,
                                 'id': randomword(5)
                                 }
                                )


register.tag(User_comment_Likes)
