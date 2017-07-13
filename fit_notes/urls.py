from django.conf.urls import url

from fit_notes.views import FitView


urlpatterns = [
    url(r'^fit-notes/$', FitView.as_view(), name='fit-notes'),
]