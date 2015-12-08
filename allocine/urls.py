from django.conf.urls import url
from allocine import views

urlpatterns = [
    url(r'^cinemas/$', views.AllocineCinema.as_view(), name='cinema-query'),
    url(r'^movie/$', views.AllocineMovie.as_view(), name='movie-query'),
    url(r'^showtimes/$', views.AllocineShowtime.as_view(), name='showtime-query'),
]