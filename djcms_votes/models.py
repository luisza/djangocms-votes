from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from cms.models.pagemodel import Page
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


def get_app_name_models(model):
    return "{0}.{1}".format(model._meta.app_label, model._meta.object_name).lower()


class Comment(models.Model):
    POSITIVE = 1
    NEGATIVE = 2
    NEUTRAL = 3
    TYPES = (
        (POSITIVE, _("Positive")),
        (NEGATIVE, _("Negative")),
        (NEUTRAL, _("Neutral")),
    )

    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    message = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    comment_type = models.SmallIntegerField(choices=TYPES, default=NEUTRAL)

    def __str__(self):
        return "%s wrote at %s" % (self.user.get_full_name(),
                                   self.created_date.strftime("%b %d %Y %H:%M:%S"))


class Poll(models.Model):

    ZERO = 0
    TYPES = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    poll_type = models.SmallIntegerField(choices=TYPES, default=ZERO)

    def __str__(self):
        return "%s wrote at %s" % (self.user.get_full_name(),
                                   self.created_date.strftime("%b %d %Y %H:%M:%S"))
