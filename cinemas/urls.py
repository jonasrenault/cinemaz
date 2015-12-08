from django.conf.urls import url, include
from cinemas import views


urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^cinemas/$', views.CinemaList.as_view(), name='cinema-list'),
    url(r'^movies/$', views.MovieList.as_view(), name='movie-list'),
    url(r'^import/cinema/$', views.import_cinemas),
    url(r'^import/showtime/$', views.get_show_times),
]