

from django.conf.urls import url
from djcms_votes.appviews import PollList


urlpatterns = [
    url(r'$', PollList.as_view(), name="app_poll_list"),

]
