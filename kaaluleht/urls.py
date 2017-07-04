from django.conf.urls import url

from kaaluleht.views import DashboardView, DetailView


urlpatterns = [
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^users/(?P<pk>[0-9]+)-(?P<slug>[-\w]*)/$', DetailView.as_view(), name='detail'),
]
