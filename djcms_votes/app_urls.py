

from django.conf.urls import url
from djcms_votes.appviews import BucketView


urlpatterns = [
    url(r'$', BucketView.as_view(), name="app_poll_list"),

]
