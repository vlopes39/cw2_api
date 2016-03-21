from django.conf.urls import url
from stock_exc_api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^indexes/$', views.IndexesList.as_view()),
    url(r'^indexes/(?P<name>[a-zA-Z0-9]+)/$', views.IndexesDetail.as_view()),
    url(r'^indexes/(?P<name>[a-zA-Z0-9]+)/country/$', views.CountryDetail.as_view()),
    url(r'^indexes/(?P<name>[a-zA-Z0-9]+)/country/indexes/$', views.IndexesListPerCountry.as_view()),
    url(r'^indexes/(?P<name>[a-zA-Z0-9]+)/hist/$', views.HistData.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)