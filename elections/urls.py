from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^poll/(?P<document>\d+)$', views.Poll.as_view(), name='poll'),
    url(r'^vote/(?P<document>\d+)$', views.Vote.as_view(), name='vote'),
    url(r'^report/$', views.Report.as_view(), name='report'),
    url(r'^report/election/(?P<pk>\d+)$',
        views.ElectionDetail.as_view(),
        name='election-detail'),
    url(r'^report/csv/election/(?P<pk>\d+)$',
        views.download_csv,
        name='election-csv'),
    url(r'^report/election/station/(?P<pk>\d+)$',
        views.PollingStationDetail.as_view(),
        name='station-detail'),
    url(r'^votes/$', views.QueryVotesView.as_view(), name='query-votes'),
    url(r'^votes/(?P<document>\d+)$', views.VoteReport.as_view(),
        name='votes-report'),
]
