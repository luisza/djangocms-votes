
from django.conf.urls import include, url
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^votes/', include('djcms_votes.urls')),
]
