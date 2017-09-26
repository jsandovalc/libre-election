from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^poll/(?P<document>\d+)$', views.Poll.as_view(), name='poll'),
    url(r'^vote/(?P<document>\d+)$', views.Vote.as_view(), name='vote'),
]
