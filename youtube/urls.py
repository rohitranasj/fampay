from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get-latest-videos/$', views.GetLatestVideosView.as_view()),
    url(r'^search-videos/$', views.SearchVideosView.as_view()),
    url(r'^create-index/$', views.CreateESIndexView.as_view()),
]
