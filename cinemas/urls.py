from django.conf.urls import url, include
from cinemas import views


urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^cinemas/$', views.CinemaList.as_view(), name='cinema-list'),
    url(r'^cinemas/import/$', views.ImportCinema.as_view(), name='cinema-import'),
    url(r'^movies/$', views.MovieList.as_view(), name='movie-list'),
    url(r'^movies/import/$', views.ImportMovie.as_view(), name='movie-import'),
]